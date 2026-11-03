from datetime import datetime, timedelta, timezone
import json
from typing import Dict, Any, List, Optional
from app.db.database import db
from app.models.domain import PriorityLevel, AnnouncementCategory
from app.models.schemas import AnnouncementResponse, DigestResponse

class DigestService:
    @classmethod
    def get_windowed_digest(cls, window_hours: int = 24, ticker: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves announcements within the window (default 24h).
        Sorts and splits into material (promoted) and routine (collapsed).
        """
        now = datetime.now(timezone.utc)
        start_time = (now - timedelta(hours=window_hours)).isoformat()

        query = """
        SELECT a.*, c.name as comp_name
        FROM announcements a
        LEFT JOIN companies c ON a.ticker = c.ticker
        WHERE a.broadcast_time >= ?
        """
        params = [start_time]

        if ticker:
            query += " AND a.ticker = ?"
            params.append(ticker)

        query += " ORDER BY a.materiality_score DESC, a.broadcast_time DESC"

        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

        material_list = []
        routine_list = []

        for r in rows:
            enriched = json.loads(r["enriched_data"]) if r["enriched_data"] else None
            item = AnnouncementResponse(
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
            )

            if item.priority_level in [PriorityLevel.HIGH, PriorityLevel.MEDIUM]:
                material_list.append(item)
            else:
                routine_list.append(item)

        return {
            "window_hours": window_hours,
            "generated_at": now,
            "total_announcements": len(material_list) + len(routine_list),
            "material_count": len(material_list),
            "routine_count": len(routine_list),
            "material_announcements": material_list,
            "routine_announcements": routine_list
        }

digest_service = DigestService()
