from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.db.database import db
from app.services.market_data import MarketDataService, market_service
from app.models.schemas import CompanyListResponse, CompanyResponse

router = APIRouter()

@router.get("", response_model=CompanyListResponse)
def get_portfolio():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM companies WHERE is_in_portfolio = 1 ORDER BY ticker ASC")
        rows = cursor.fetchall()

    companies = []
    for r in rows:
        ticker = r["ticker"]
        # Fetch EOD metrics
        metrics = market_service.get_eod_metrics(ticker)
        
        # Fetch latest announcement
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title, broadcast_time FROM announcements WHERE ticker = ? ORDER BY broadcast_time DESC LIMIT 1", (ticker,))
            ann = cursor.fetchone()

        companies.append(CompanyResponse(
            ticker=ticker,
            name=r["name"],
            sector=r["sector"],
            market_cap_category=r["market_cap_category"],
            is_in_portfolio=bool(r["is_in_portfolio"]),
            last_price=metrics.get("current_price"),
            change_pct=metrics.get("change_pct"),
            volume=metrics.get("volume"),
            volume_sma_20=int(metrics.get("volume_sma_20", 0)),
            volume_ratio=metrics.get("volume_ratio"),
            latest_announcement_date=str(ann["broadcast_time"])[:10] if ann else None,
            latest_announcement_title=ann["title"] if ann else None
        ))

    return CompanyListResponse(total=len(companies), companies=companies)

@router.post("/{ticker}")
def add_to_portfolio(ticker: str, name: Optional[str] = None, sector: Optional[str] = "Equity"):
    norm_ticker = MarketDataService.normalize_ticker(ticker)
    comp_name = name or norm_ticker.replace(".NS", "")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO companies (ticker, name, sector, market_cap_category, is_in_portfolio, created_at)
        VALUES (?, ?, ?, 'Mid', 1, datetime('now'))
        """, (norm_ticker, comp_name, sector))
        conn.commit()
    return {"status": "success", "message": f"{norm_ticker} added to portfolio"}
