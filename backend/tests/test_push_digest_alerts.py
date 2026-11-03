import pytest
import uuid
from app.services.digest_service import DigestService
from app.services.alert_service import AlertService
from app.models.schemas import AlertConfigModel
from app.models.domain import AnnouncementCategory

def test_windowed_digest_24h():
    digest = DigestService.get_windowed_digest(window_hours=24)
    assert digest["window_hours"] == 24
    assert digest["total_announcements"] > 0
    assert digest["material_count"] > 0
    assert digest["routine_count"] > 0
    material_categories = [a.category for a in digest["material_announcements"]]
    assert AnnouncementCategory.MANAGEMENT_CHANGE in material_categories or AnnouncementCategory.RESULTS in material_categories
    routine_categories = [a.category for a in digest["routine_announcements"]]
    assert AnnouncementCategory.UNCLASSIFIED in routine_categories

def test_digest_window_expansion():
    digest_24h = DigestService.get_windowed_digest(window_hours=24)
    digest_168h = DigestService.get_windowed_digest(window_hours=168)
    assert digest_168h["total_announcements"] >= digest_24h["total_announcements"]

def test_alert_config_get_and_update():
    fresh_user_id = f"test_user_{uuid.uuid4().hex[:8]}"
    cfg = AlertService.get_config(fresh_user_id)
    assert cfg.price_change_threshold_pct == 3.0
    
    # Update config
    cfg.price_change_threshold_pct = 4.5
    cfg.volume_surge_multiplier = 2.5
    updated = AlertService.update_config(cfg)
    assert updated.price_change_threshold_pct == 4.5
    
    # Re-fetch
    fetched = AlertService.get_config(fresh_user_id)
    assert fetched.price_change_threshold_pct == 4.5
    assert fetched.volume_surge_multiplier == 2.5

def test_alerts_feed():
    feed = AlertService.get_alerts_feed(limit=10)
    assert len(feed) > 0
    top = feed[0]
    assert top.headline != ""
    assert top.severity in ["CRITICAL", "WARNING", "INFO"]
    
    AlertService.mark_as_read(top.id)
    feed_unread = AlertService.get_alerts_feed(unread_only=True)
    assert top.id not in [a.id for a in feed_unread]
