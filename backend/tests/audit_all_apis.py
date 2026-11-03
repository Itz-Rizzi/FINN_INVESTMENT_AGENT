import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

endpoints = [
    ("GET", "/health", None),
    ("GET", "/portfolio", None),
    ("POST", "/portfolio/TRENT.NS", None),
    ("GET", "/announcements?limit=10", None),
    ("POST", "/announcements/classify", {
        "ticker": "RELIANCE.NS",
        "title": "Board approves acquisition of renewable energy asset",
        "text_snippet": "Reliance New Energy has entered into an agreement to acquire 100% equity stake."
    }),
    ("POST", "/announcements/sync", {"lookback_days": 2}),
    ("GET", "/digest?window_hours=24", None),
    ("GET", "/alerts/feed", None),
    ("GET", "/alerts/config", None),
    ("PUT", "/alerts/config", {
        "user_id": "default_investor",
        "price_change_threshold_pct": 3.0,
        "volume_surge_multiplier": 2.0,
        "notify_categories": ["results", "M&A", "management_change"],
        "is_active": True
    }),
    ("POST", "/alerts/scan", {}),
    ("GET", "/results/TRENT", None),
    ("GET", "/research/RELIANCE/snapshot", None),
    ("GET", "/research/RELIANCE/narrative-vs-numbers", None),
    ("POST", "/copilot/query", {
        "ticker": "TRENT.NS",
        "query": "What drove Trent's EBITDA margin expansion in Q2?",
        "conversation_history": []
    })
]

print("="*60)
print("AUDITING ALL 15 MAJOR REST APIS")
print("="*60)

results = []
for method, ep, payload in endpoints:
    url = f"{BASE_URL}{ep}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            elapsed_ms = int((time.time() - t0) * 1000)
            body = json.loads(resp.read().decode("utf-8"))
            status = resp.status
            results.append((method, ep, status, elapsed_ms, "PASS"))
            print(f"[{status}] {method:<5} {ep:<45} {elapsed_ms:>4}ms -> PASS")
    except urllib.error.HTTPError as e:
        elapsed_ms = int((time.time() - t0) * 1000)
        results.append((method, ep, e.code, elapsed_ms, "FAIL"))
        print(f"[{e.code}] {method:<5} {ep:<45} {elapsed_ms:>4}ms -> FAIL ({e.reason})")
    except Exception as e:
        elapsed_ms = int((time.time() - t0) * 1000)
        results.append((method, ep, 500, elapsed_ms, "ERROR"))
        print(f"[ERR] {method:<5} {ep:<45} {elapsed_ms:>4}ms -> ERROR ({e})")

print("="*60)
all_pass = all(r[4] == "PASS" for r in results)
print(f"OVERALL API AUDIT RESULT: {'ALL PASS (15/15)' if all_pass else 'SOME FAILED'}")
print("="*60)
