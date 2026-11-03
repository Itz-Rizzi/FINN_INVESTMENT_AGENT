from fastapi import APIRouter, Query, HTTPException, BackgroundTasks
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import json
from app.db.database import db
from app.services.classifier import classifier_service
from app.services.announcement_feeder import announcement_feeder
from app.models.schemas import AnnouncementResponse, AnnouncementClassifyRequest, AnnouncementClassifyResponse
from app.models.domain import AnnouncementCategory, PriorityLevel

router = APIRouter()

@router.get("", response_model=List[AnnouncementResponse])
def list_announcements(
    ticker: Optional[str] = None,
    category: Optional[str] = None,
    material_only: bool = False,
    limit: int = Query(50, ge=1, le=200)
):
    query = """
    SELECT a.*, c.name as comp_name
    FROM announcements a
    LEFT JOIN companies c ON a.ticker = c.ticker
    WHERE 1=1
    """
    params = []
    if ticker:
        query += " AND a.ticker = ?"
        params.append(ticker)
    if category:
        query += " AND a.category = ?"
        params.append(category)
    if material_only:
        query += " AND a.is_material = 1"
    
    query += " ORDER BY a.broadcast_time DESC LIMIT ?"
    params.append(limit)

    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

    results = []
    for r in rows:
        enriched = json.loads(r["enriched_data"]) if r["enriched_data"] else None
        results.append(AnnouncementResponse(
            id=r["id"],
            ticker=r["ticker"],
            company_name=r["comp_name"] or r["company_name"],
            broadcast_time=datetime.fromisoformat(r["broadcast_time"]),
            category=AnnouncementCategory(r["category"]),
            title=r["title"],
            attachment_url=r["attachment_url"],
            is_material=bool(r["is_material"]),
            materiality_score=float(r["materiality_score"]),
            priority_level=PriorityLevel(r["priority_level"]),
            one_line_summary=r["one_line_summary"],
            enriched_data=enriched
        ))
    return results

@router.post("/classify", response_model=AnnouncementClassifyResponse)
def classify_announcement(req: AnnouncementClassifyRequest):
    res = classifier_service.classify_announcement(req.ticker, req.title, req.text_snippet or "")
    return AnnouncementClassifyResponse(
        category=res["category"],
        confidence=res["confidence"],
        priority_level=res["priority_level"],
        is_material=res["is_material"],
        one_line_summary=res["one_line_summary"],
        reasoning=res["reasoning"]
    )

@router.post("/sync")
def sync_live_announcements(
    symbol: Optional[str] = Query(None, description="Optional single ticker to sync, or all portfolio if omitted"),
    limit_per_stock: int = Query(5, ge=1, le=20)
) -> Dict[str, Any]:
    """
    Polls the live official NSE exchange announcement feed,
    classifies filings, deduplicates by ID/URL, and updates the database.
    """
    if symbol:
        clean_sym = symbol.strip().upper()
        if not clean_sym.endswith(".NS") and not clean_sym.endswith(".BO"):
            clean_sym = f"{clean_sym}.NS"
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM companies WHERE ticker = ?", (clean_sym,))
            row = cursor.fetchone()
            comp_name = row["name"] if row else clean_sym.replace(".NS", "")

        raw_items = announcement_feeder.fetch_live_announcements(clean_sym)
        inserted = 0
        for item in raw_items[:limit_per_stock]:
            if announcement_feeder._process_and_save_item(clean_sym, comp_name, item):
                inserted += 1

        return {
            "status": "success",
            "symbol": clean_sym,
            "total_fetched": len(raw_items),
            "new_inserted": inserted
        }
    else:
        return announcement_feeder.ingest_announcements_for_portfolio(limit_per_stock=limit_per_stock)
