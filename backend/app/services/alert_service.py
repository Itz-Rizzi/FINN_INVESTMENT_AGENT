from datetime import datetime, timezone
import json
import uuid
from typing import List, Dict, Any, Optional
from app.db.database import db
from app.models.domain import AlertType, AnnouncementCategory
from app.models.schemas import AlertConfigModel, TriggeredAlertResponse

class AlertService:
    @classmethod
    def get_config(cls, user_id: str = "default_investor") -> AlertConfigModel:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alert_configs WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                cats = json.loads(row["notify_categories"]) if row["notify_categories"] else []
                return AlertConfigModel(
                    user_id=row["user_id"],
                    price_change_threshold_pct=row["price_change_threshold_pct"],
                    volume_surge_multiplier=row["volume_surge_multiplier"],
                    notify_categories=[AnnouncementCategory(c) for c in cats if c in [ac.value for ac in AnnouncementCategory]],
                    is_active=bool(row["is_active"])
                )
        return AlertConfigModel(user_id=user_id)

    @classmethod
    def update_config(cls, config: AlertConfigModel) -> AlertConfigModel:
        now_iso = datetime.now(timezone.utc).isoformat()
        cats_json = json.dumps([c.value for c in config.notify_categories])
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO alert_configs (id, user_id, price_change_threshold_pct, volume_surge_multiplier, notify_categories, is_active, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (f"config_{config.user_id}", config.user_id, config.price_change_threshold_pct, config.volume_surge_multiplier, cats_json, int(config.is_active), now_iso))
            conn.commit()
        return config

    @classmethod
    def get_alerts_feed(cls, limit: int = 50, unread_only: bool = False) -> List[TriggeredAlertResponse]:
        query = "SELECT * FROM triggered_alerts"
        params = []
        if unread_only:
            query += " WHERE is_read = 0"
        query += " ORDER BY triggered_at DESC LIMIT ?"
        params.append(limit)

        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

        alerts = []
        for r in rows:
            metrics_dict = json.loads(r["metrics"]) if r["metrics"] else {}
            alerts.append(TriggeredAlertResponse(
                id=r["id"],
                ticker=r["ticker"],
                company_name=r["company_name"],
                alert_type=AlertType(r["alert_type"]),
                severity=r["severity"],
                headline=r["headline"],
                details=r["details"],
                metrics=metrics_dict,
                triggered_at=datetime.fromisoformat(r["triggered_at"]),
                is_read=bool(r["is_read"])
            ))
        return alerts

    @classmethod
    def mark_as_read(cls, alert_id: str):
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE triggered_alerts SET is_read = 1 WHERE id = ?", (alert_id,))
            conn.commit()

alert_service = AlertService()
