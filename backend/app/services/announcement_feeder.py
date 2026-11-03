import json
import hashlib
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from curl_cffi import requests

from app.db.database import db
from app.services.classifier import classifier_service
from app.models.domain import AnnouncementCategory, PriorityLevel

logger = logging.getLogger(__name__)

class AnnouncementFeederService:
    def __init__(self):
        self.base_url = "https://www.nseindia.com"
        self.announcements_url = "https://www.nseindia.com/api/corporate-announcements?index=equities"
        self.session: Optional[requests.Session] = None
        self._init_session()

    def _init_session(self):
        """Initializes a browser-impersonated session with NSE cookies."""
        try:
            self.session = requests.Session(impersonate="chrome120")
            # Warm up home page to receive initial cookies
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            }
            res = self.session.get(self.base_url, headers=headers, timeout=10)
            if res.status_code == 200:
                logger.info("NSE session initialized successfully.")
            else:
                logger.warning(f"NSE session init returned status {res.status_code}")
        except Exception as e:
            logger.error(f"Error initializing NSE session: {e}")
            self.session = None

    def fetch_live_announcements(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetches live corporate announcements from the official NSE API.
        If symbol is provided (e.g. 'TRENT' or 'TRENT.NS'), fetches specifically for that stock.
        """
        if not self.session:
            self._init_session()

        clean_symbol = symbol.replace(".NS", "").replace(".BO", "").strip().upper() if symbol else None
        url = f"{self.announcements_url}&symbol={clean_symbol}" if clean_symbol else self.announcements_url
        
        headers = {
            "Referer": "https://www.nseindia.com/companies-listing/corporate-filings-announcements",
            "Accept": "application/json, text/plain, */*",
        }

        try:
            res = self.session.get(url, headers=headers, timeout=12)
            if res.status_code == 403 or res.status_code == 401:
                logger.info("Refreshing NSE session after 403...")
                self._init_session()
                res = self.session.get(url, headers=headers, timeout=12)

            if res.status_code != 200:
                logger.warning(f"NSE announcements API returned status {res.status_code}")
                return []

            data = res.json()
            if not isinstance(data, list):
                logger.warning("Unexpected non-list response from NSE announcements API")
                return []

            return data

        except Exception as e:
            logger.error(f"Error fetching live announcements from NSE for {clean_symbol or 'all'}: {e}")
            return []

    def ingest_announcements_for_portfolio(self, limit_per_stock: int = 5) -> Dict[str, Any]:
        """
        Polls official NSE announcements for all active portfolio stocks,
        classifies them, deduplicates, and saves them to the SQLite database.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ticker, name FROM companies WHERE is_in_portfolio = 1")
            portfolio = cursor.fetchall()

        total_fetched = 0
        total_inserted = 0

        for comp in portfolio:
            ticker = comp["ticker"]
            comp_name = comp["name"]
            raw_items = self.fetch_live_announcements(ticker)
            total_fetched += len(raw_items)

            for item in raw_items[:limit_per_stock]:
                inserted = self._process_and_save_item(ticker, comp_name, item)
                if inserted:
                    total_inserted += 1

        logger.info(f"Ingested {total_inserted} new announcements across portfolio from {total_fetched} live items.")
        return {
            "status": "success",
            "total_fetched": total_fetched,
            "total_new_inserted": total_inserted
        }

    def _process_and_save_item(self, ticker: str, company_name: str, raw_item: Dict[str, Any]) -> bool:
        """
        Deduplicates, classifies, and inserts a single live announcement into SQLite.
        """
        title = raw_item.get("desc") or raw_item.get("attchmntText") or "Corporate Filing"
        snippet = raw_item.get("attchmntText", "")
        attachment_url = raw_item.get("attchmntFile")
        seq_id = str(raw_item.get("seq_id") or "")

        # Parse broadcast time (format: "03-Nov-2026 14:45:26" or "2026-11-03 14:45:26")
        raw_dt = raw_item.get("sort_date") or raw_item.get("an_dt") or ""
        broadcast_iso = self._parse_nse_datetime(raw_dt)

        # Generate stable deterministic unique identifier for deduplication
        if seq_id:
            ann_id = f"nse_{seq_id}"
        else:
            hash_input = f"{ticker}_{title}_{broadcast_iso}".encode("utf-8")
            ann_id = f"nse_{hashlib.sha256(hash_input).hexdigest()[:16]}"

        # Check if already exists in database
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM announcements WHERE id = ?", (ann_id,))
            if cursor.fetchone():
                return False  # Already present, prevent duplicate

        # AI & Rule-based 17-category classification
        classification = classifier_service.classify_announcement(ticker, title, snippet)
        category = classification["category"].value
        priority = classification["priority_level"].value
        is_material = 1 if classification["is_material"] else 0
        mat_score = float(classification["materiality_score"])
        summary = classification["one_line_summary"]

        now_iso = datetime.now(timezone.utc).isoformat()
        enriched_data_json = json.dumps({
            "exchange": "NSE",
            "seq_id": seq_id,
            "industry": raw_item.get("smIndustry"),
            "file_size": raw_item.get("attFileSize"),
            "raw_desc": raw_item.get("desc"),
            "raw_snippet": snippet[:300]
        })

        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO announcements (
                id, ticker, company_name, broadcast_time, category, title, attachment_url,
                local_pdf_path, is_material, materiality_score, priority_level, one_line_summary,
                enriched_data, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?, ?, ?)
            """, (
                ann_id, ticker, company_name, broadcast_iso, category, title, attachment_url,
                is_material, mat_score, priority, summary, enriched_data_json, now_iso
            ))
            conn.commit()

        return True

    @staticmethod
    def _parse_nse_datetime(dt_str: str) -> str:
        """Normalizes various NSE date formats to ISO-8601 string."""
        if not dt_str:
            return datetime.now(timezone.utc).isoformat()
        
        # Try format: "2026-11-03 14:45:26"
        for fmt in ("%Y-%m-%d %H:%M:%S", "%d-%b-%Y %H:%M:%S", "%d-%b-%Y %H:%M"):
            try:
                dt = datetime.strptime(dt_str.strip(), fmt)
                # Assume IST (UTC+5:30)
                ist_offset = timezone(timedelta(hours=5, minutes=30))
                dt = dt.replace(tzinfo=ist_offset)
                return dt.astimezone(timezone.utc).isoformat()
            except ValueError:
                continue
        
        return datetime.now(timezone.utc).isoformat()

announcement_feeder = AnnouncementFeederService()
