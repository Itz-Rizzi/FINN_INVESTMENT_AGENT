from fastapi import APIRouter
from typing import List
from app.services.alert_service import alert_service
from app.services.market_data import market_service
from app.models.schemas import AlertConfigModel, TriggeredAlertResponse

router = APIRouter()

@router.get("/feed", response_model=List[TriggeredAlertResponse])
def get_alerts_feed(limit: int = 50, unread_only: bool = False):
    return alert_service.get_alerts_feed(limit=limit, unread_only=unread_only)

@router.get("/config", response_model=AlertConfigModel)
def get_alert_config(user_id: str = "default_investor"):
    return alert_service.get_config(user_id=user_id)

@router.put("/config", response_model=AlertConfigModel)
def update_alert_config(config: AlertConfigModel):
    return alert_service.update_config(config)

@router.post("/{alert_id}/read")
def mark_alert_read(alert_id: str):
    alert_service.mark_as_read(alert_id)
    return {"status": "success", "alert_id": alert_id}

@router.post("/scan")
def scan_alerts():
    new_alerts = market_service.scan_and_trigger_alerts()
    return {"status": "success", "triggered_count": len(new_alerts), "alerts": new_alerts}
