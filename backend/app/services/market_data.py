import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import json
import uuid
import logging
from typing import Dict, Any, List, Optional

from app.db.database import db
from app.models.domain import AlertType

logger = logging.getLogger(__name__)

MOCK_MARKET_BASELINE = {
    "RELIANCE.NS": {"price": 1290.90, "sma_vol": 12500000},
    "TCS.NS": {"price": 4120.50, "sma_vol": 2100000},
    "HDFCBANK.NS": {"price": 1745.20, "sma_vol": 16400000},
    "INFY.NS": {"price": 1860.40, "sma_vol": 6200000},
    "ICICIBANK.NS": {"price": 1285.60, "sma_vol": 14200000},
    "TITAN.NS": {"price": 3290.00, "sma_vol": 1100000},
    "TATAMOTORS.NS": {"price": 845.30, "sma_vol": 9500000},
    "LT.NS": {"price": 3610.00, "sma_vol": 2300000},
    "ITC.NS": {"price": 482.50, "sma_vol": 11800000},
    "SUNPHARMA.NS": {"price": 1820.00, "sma_vol": 2600000},
    "TRENT.NS": {"price": 7240.00, "sma_vol": 1850000},
    "DIXON.NS": {"price": 14850.00, "sma_vol": 1150000},
    "POLYCAB.NS": {"price": 6890.00, "sma_vol": 890000},
    "ZOMATO.NS": {"price": 262.50, "sma_vol": 42000000},
    "KPITTECH.NS": {"price": 1720.00, "sma_vol": 1450000},
    "CDSL.NS": {"price": 1580.00, "sma_vol": 2800000},
    "SUZLON.NS": {"price": 68.40, "sma_vol": 58000000},
}

class MarketDataService:
    # In-memory fast cache: {ticker: (timestamp, metrics)}
    _memory_cache: Dict[str, Any] = {}

    @staticmethod
    def normalize_ticker(ticker: str) -> str:
        clean = ticker.strip().upper()
        if not clean.endswith(".NS") and not clean.endswith(".BO"):
            clean = f"{clean}.NS"
        return clean

    @classmethod
    def get_eod_metrics(
        cls, 
        ticker: str, 
        price_threshold: float = 3.0, 
        volume_threshold: float = 2.0
    ) -> Dict[str, Any]:
        symbol = cls.normalize_ticker(ticker)
        now = datetime.now(timezone.utc)

        # 1. Check in-memory cache (TTL: 10 minutes)
        if symbol in cls._memory_cache:
            cached_time, cached_val = cls._memory_cache[symbol]
            if (now - cached_time) < timedelta(minutes=10):
                # Recalculate unusual flags with current thresholds
                cached_val["is_volume_unusual"] = cached_val["volume_ratio"] >= volume_threshold
                cached_val["is_price_unusual"] = abs(cached_val["change_pct"]) >= price_threshold
                return cached_val

        # 2. Check DB cache
        db_cached = cls._get_db_cache(symbol, price_threshold, volume_threshold)
        if db_cached:
            cls._memory_cache[symbol] = (now, db_cached)
            return db_cached

        # 3. Live fetch via yfinance
        try:
            yt = yf.Ticker(symbol)
            hist = yt.history(period="1mo")
            
            if hist.empty or len(hist) < 2:
                fallback = cls._get_fallback(symbol, price_threshold, volume_threshold)
                cls._memory_cache[symbol] = (now, fallback)
                return fallback

            closes = hist["Close"].tolist()
            volumes = hist["Volume"].tolist()
            
            latest_price = round(float(closes[-1]), 2)
            prev_price = round(float(closes[-2]), 2)
            change_pct = round(((latest_price - prev_price) / prev_price) * 100, 2)
            
            latest_volume = int(volumes[-1])
            sma_window = volumes[-21:-1] if len(volumes) >= 21 else volumes[:-1]
            volume_sma_20 = round(float(np.mean(sma_window)), 0) if sma_window else latest_volume
            volume_ratio = round(latest_volume / volume_sma_20, 2) if volume_sma_20 > 0 else 1.0

            history_items = []
            for date_idx, row in hist.tail(10).iterrows():
                trade_date_str = str(date_idx)[:10]
                history_items.append({
                    "trade_date": trade_date_str,
                    "open": round(float(row["Open"]), 2),
                    "high": round(float(row["High"]), 2),
                    "low": round(float(row["Low"]), 2),
                    "close": round(float(row["Close"]), 2),
                    "volume": int(row["Volume"]),
                })

            is_volume_unusual = volume_ratio >= volume_threshold
            is_price_unusual = abs(change_pct) >= price_threshold

            cls._cache_eod_price(symbol, history_items[-1]["trade_date"], history_items[-1]["open"],
                                history_items[-1]["high"], history_items[-1]["low"], latest_price,
                                latest_volume, volume_sma_20, change_pct)

            result = {
                "ticker": symbol,
                "current_price": latest_price,
                "change_pct": change_pct,
                "volume": latest_volume,
                "volume_sma_20": volume_sma_20,
                "volume_ratio": volume_ratio,
                "is_volume_unusual": is_volume_unusual,
                "is_price_unusual": is_price_unusual,
                "history": history_items
            }
            cls._memory_cache[symbol] = (now, result)
            return result

        except Exception as e:
            logger.warning(f"Error fetching live data for {symbol}: {e}. Using fallback.")
            fallback = cls._get_fallback(symbol, price_threshold, volume_threshold)
            cls._memory_cache[symbol] = (now, fallback)
            return fallback

    @classmethod
    def _cache_eod_price(cls, ticker, trade_date, o, h, l, c, vol, sma, chg):
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT OR REPLACE INTO eod_prices (id, ticker, trade_date, open_price, high_price, low_price, close_price, volume, volume_sma_20, daily_change_pct)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (f"{ticker}_{trade_date}", ticker, trade_date, o, h, l, c, vol, sma, chg))
                conn.commit()
        except Exception:
            pass

    @classmethod
    def _get_db_cache(cls, symbol: str, price_threshold: float, volume_threshold: float) -> Optional[Dict[str, Any]]:
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM eod_prices WHERE ticker = ? ORDER BY trade_date DESC LIMIT 1", (symbol,))
                row = cursor.fetchone()
                if row:
                    ratio = round(row["volume"] / row["volume_sma_20"], 2) if row["volume_sma_20"] else 1.0
                    return {
                        "ticker": symbol,
                        "current_price": row["close_price"],
                        "change_pct": row["daily_change_pct"],
                        "volume": row["volume"],
                        "volume_sma_20": row["volume_sma_20"],
                        "volume_ratio": ratio,
                        "is_volume_unusual": ratio >= volume_threshold,
                        "is_price_unusual": abs(row["daily_change_pct"]) >= price_threshold,
                        "history": []
                    }
        except Exception:
            pass
        return None

    @classmethod
    def _get_fallback(cls, symbol: str, price_threshold: float, volume_threshold: float) -> Dict[str, Any]:
        baseline = MOCK_MARKET_BASELINE.get(symbol, {"price": 1000.0, "sma_vol": 1000000})
        price = baseline["price"]
        sma_vol = baseline["sma_vol"]
        ratio = 1.15
        return {
            "ticker": symbol,
            "current_price": price,
            "change_pct": 1.25,
            "volume": int(sma_vol * ratio),
            "volume_sma_20": sma_vol,
            "volume_ratio": ratio,
            "is_volume_unusual": ratio >= volume_threshold,
            "is_price_unusual": False,
            "history": []
        }

    @classmethod
    def scan_and_trigger_alerts(cls, user_id: str = "default_investor") -> List[Dict[str, Any]]:
        new_alerts = []
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alert_configs WHERE user_id = ? AND is_active = 1", (user_id,))
            config = cursor.fetchone()
            
            p_threshold = config["price_change_threshold_pct"] if config else 3.0
            v_threshold = config["volume_surge_multiplier"] if config else 2.0

            cursor.execute("SELECT ticker, name FROM companies WHERE is_in_portfolio = 1")
            companies = cursor.fetchall()

        now_iso = datetime.now(timezone.utc).isoformat()

        for comp in companies:
            ticker = comp["ticker"]
            name = comp["name"]
            metrics = cls.get_eod_metrics(ticker, p_threshold, v_threshold)

            if metrics["is_volume_unusual"]:
                alert_id = str(uuid.uuid4())
                headline = f"Unusual Volume Surge: {metrics['volume_ratio']}× 20-Day SMA"
                details = f"{name} traded {metrics['volume']:,} shares today vs. 20-day average of {int(metrics['volume_sma_20']):,} shares ({int((metrics['volume_ratio']-1)*100)}% surge)."
                cls._save_triggered_alert(alert_id, ticker, name, AlertType.VOLUME_SURGE.value, "WARNING", headline, details, {
                    "volume": metrics["volume"],
                    "volume_sma_20": metrics["volume_sma_20"],
                    "volume_ratio": metrics["volume_ratio"]
                }, now_iso)
                new_alerts.append({"ticker": ticker, "headline": headline, "type": "VOLUME_SURGE"})

            if metrics["is_price_unusual"]:
                alert_id = str(uuid.uuid4())
                direction = "+" if metrics["change_pct"] > 0 else ""
                severity = "CRITICAL" if abs(metrics["change_pct"]) >= p_threshold * 1.5 else "INFO"
                headline = f"Price Move Alert: {direction}{metrics['change_pct']}% Daily Move"
                details = f"{name} moved {direction}{metrics['change_pct']}% to close at Rs {metrics['current_price']:,} crossing your {p_threshold}% threshold."
                cls._save_triggered_alert(alert_id, ticker, name, AlertType.PRICE_SWING.value, severity, headline, details, {
                    "price": metrics["current_price"],
                    "change_pct": metrics["change_pct"],
                    "threshold_pct": p_threshold
                }, now_iso)
                new_alerts.append({"ticker": ticker, "headline": headline, "type": "PRICE_SWING"})

        return new_alerts

    @classmethod
    def _save_triggered_alert(cls, alert_id, ticker, name, a_type, severity, headline, details, metrics_dict, triggered_at):
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO triggered_alerts (id, ticker, company_name, alert_type, severity, headline, details, metrics, is_read, triggered_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
                """, (alert_id, ticker, name, a_type, severity, headline, details, json.dumps(metrics_dict), triggered_at))
                conn.commit()
        except Exception:
            pass

market_service = MarketDataService()
