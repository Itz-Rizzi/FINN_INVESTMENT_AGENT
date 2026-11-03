import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_and_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "healthy"}

def test_portfolio_endpoint():
    res = client.get("/api/v1/portfolio")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 15
    tickers = [c["ticker"] for c in data["companies"]]
    assert "RELIANCE.NS" in tickers
    assert "TRENT.NS" in tickers

def test_digest_endpoint():
    res = client.get("/api/v1/digest?window_hours=24")
    assert res.status_code == 200
    data = res.json()
    assert data["window_hours"] == 24
    assert "material_announcements" in data
    assert "routine_announcements" in data
    assert data["material_count"] >= 1

def test_classify_endpoint():
    payload = {
        "ticker": "TITAN.NS",
        "title": "Intimation of Appointment of Chief Financial Officer under Reg 30"
    }
    res = client.post("/api/v1/announcements/classify", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["category"] == "management_change"
    assert data["priority_level"] == "HIGH"

def test_alerts_endpoints():
    res_feed = client.get("/api/v1/alerts/feed")
    assert res_feed.status_code == 200
    feed = res_feed.json()
    assert len(feed) > 0

    res_cfg = client.get("/api/v1/alerts/config")
    assert res_cfg.status_code == 200
    cfg = res_cfg.json()
    assert "price_change_threshold_pct" in cfg

def test_quarterly_results_endpoint():
    res = client.get("/api/v1/results/TRENT.NS")
    assert res.status_code == 200
    data = res.json()
    assert data["ticker"] == "TRENT.NS"
    curr = data["current_quarter"]
    assert curr["revenue_cr"] > 0
    assert curr["ebitda_margin_pct"] > 0
    assert len(curr["citations"]) > 0

def test_narrative_vs_numbers_endpoint():
    res = client.get("/api/v1/research/TRENT.NS/narrative-vs-numbers")
    assert res.status_code == 200
    data = res.json()
    assert data["ticker"] == "TRENT.NS"
    assert data["credibility_score"] in ["HIGH", "MODERATE", "LOW"]
    assert len(data["items"]) >= 2
    for item in data["items"]:
        assert item["verdict"] in ["BEAT", "MET", "MISSED", "SHIFTED_GOALPOSTS"]
        assert item["guidance_citation"]["page_number"] > 0
        assert item["actual_citation"]["page_number"] > 0

def test_generalise_arbitrary_ticker():
    # Test arbitrary ticker outside core portfolio (BEL.NS - Bharat Electronics)
    res = client.get("/api/v1/research/BEL.NS/snapshot")
    assert res.status_code == 200
    data = res.json()
    assert data["ticker"] == "BEL.NS"
    assert "financial_snapshot" in data
    assert "cash_quality" in data
    assert "bull_vs_bear" in data

def test_copilot_grounded_query():
    payload = {
        "ticker": "TRENT.NS",
        "query": "What did management state about Zudio store additions and margins?"
    }
    res = client.post("/api/v1/copilot/query", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["answer"]) > 20
    assert len(data["citations"]) > 0
    assert len(data["suggested_followups"]) > 0
