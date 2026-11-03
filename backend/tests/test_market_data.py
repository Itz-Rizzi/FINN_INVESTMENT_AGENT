import pytest
from app.services.market_data import MarketDataService

def test_ticker_normalization():
    assert MarketDataService.normalize_ticker("reliance") == "RELIANCE.NS"
    assert MarketDataService.normalize_ticker("TCS.NS") == "TCS.NS"
    assert MarketDataService.normalize_ticker("infy.bo") == "INFY.BO"

def test_market_metrics_calculation():
    # Test with standard thresholds
    metrics = MarketDataService.get_eod_metrics("RELIANCE.NS", price_threshold=3.0, volume_threshold=2.0)
    assert "ticker" in metrics
    assert metrics["ticker"] == "RELIANCE.NS"
    assert "current_price" in metrics
    assert metrics["current_price"] > 0
    assert "volume" in metrics
    assert "volume_sma_20" in metrics
    assert "volume_ratio" in metrics
    assert isinstance(metrics["is_volume_unusual"], bool)
    assert isinstance(metrics["is_price_unusual"], bool)

def test_threshold_sensitivity():
    # If we set an impossibly high volume threshold, is_volume_unusual should be False
    metrics_strict = MarketDataService.get_eod_metrics("RELIANCE.NS", price_threshold=50.0, volume_threshold=100.0)
    assert metrics_strict["is_volume_unusual"] is False
    assert metrics_strict["is_price_unusual"] is False

    # If we set a very low threshold, it should trigger
    metrics_sensitive = MarketDataService.get_eod_metrics("RELIANCE.NS", price_threshold=0.01, volume_threshold=0.1)
    assert metrics_sensitive["is_volume_unusual"] is True

def test_arbitrary_ticker_fallback():
    # Any arbitrary ticker should return valid structure
    metrics = MarketDataService.get_eod_metrics("NONEXISTENT_XYZ_123.NS")
    assert metrics["ticker"] == "NONEXISTENT_XYZ_123.NS"
    assert metrics["current_price"] > 0
