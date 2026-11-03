import sys
import json
import urllib.request

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

base_url = 'http://127.0.0.1:8000/api/v1'

print("==========================================")
print("SECTION 5: PUSH FUNCTIONALITY AUDIT")
print("==========================================")

# 1. Daily digest & announcement prioritization
print("\n[1. Daily Digest Verification]:")
with urllib.request.urlopen(f"{base_url}/digest?window_hours=24") as resp:
    d24 = json.loads(resp.read().decode('utf-8'))
    print(f"24h Window: Total={d24['total_announcements']}, Material={d24['material_count']}, Routine={d24['routine_count']}")
    print(f"Material Announcements Promoted: {len(d24['material_announcements'])}")
    for a in d24['material_announcements'][:3]:
        print(f"  * [{a['ticker']}] Priority={a['priority_level']} | Category={a['category']} | Title='{a['title']}'")
        print(f"    Summary: '{a['one_line_summary']}'")
    print(f"Routine Noise Collapsed: {len(d24['routine_announcements'])}")
    for a in d24['routine_announcements'][:2]:
        print(f"  * [{a['ticker']}] Routine: '{a['title']}' ({a['broadcast_time']})")

with urllib.request.urlopen(f"{base_url}/digest?window_hours=168") as resp:
    d7d = json.loads(resp.read().decode('utf-8'))
    print(f"\n7-Day Window: Total={d7d['total_announcements']}, Material={d7d['material_count']}, Routine={d7d['routine_count']}")

# 2. Configurable Alert Thresholds
print("\n[2. Configurable Alert Watchdogs Verification]:")
with urllib.request.urlopen(f"{base_url}/alerts/config") as resp:
    cfg = json.loads(resp.read().decode('utf-8'))
    print(f"Current Config: Price Threshold=±{cfg['price_change_threshold_pct']}%, Volume Surge Multiplier={cfg['volume_surge_multiplier']}x SMA")

# Update thresholds
new_cfg = {
    "user_id": "default_investor",
    "price_change_threshold_pct": 2.5,
    "volume_surge_multiplier": 1.8,
    "notify_categories": ["results", "M&A", "management_change", "litigation"],
    "is_active": True
}
req = urllib.request.Request(f"{base_url}/alerts/config", data=json.dumps(new_cfg).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='PUT')
with urllib.request.urlopen(req) as resp:
    updated = json.loads(resp.read().decode('utf-8'))
    print(f"Updated Config: Price Threshold=±{updated['price_change_threshold_pct']}%, Volume Surge Multiplier={updated['volume_surge_multiplier']}x SMA")

# 3. Alert Scanning & Triggered Alerts Feed (Price Moves & Unusual Volume)
print("\n[3. Price Movement & Unusual Volume Alerts]:")
scan_req = urllib.request.Request(f"{base_url}/alerts/scan", data=b"{}", headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(scan_req) as resp:
    scan_res = json.loads(resp.read().decode('utf-8'))
    print(f"Alert Scanner Triggered: Status={scan_res.get('status')}, Scanned {scan_res.get('companies_scanned')} companies, Generated {scan_res.get('new_alerts_generated')} alerts")

with urllib.request.urlopen(f"{base_url}/alerts/feed") as resp:
    feed = json.loads(resp.read().decode('utf-8'))
    print(f"Total Triggered Alerts in Feed: {len(feed)}")
    for alert in feed[:4]:
        print(f"  * Alert [{alert['alert_type']}] for {alert['ticker']}: Severity={alert['severity']}")
        print(f"    Headline: '{alert['headline']}'")
        print(f"    Details: '{alert['details']}'")
        print(f"    Metrics: {alert['metrics']}")

# 4. Quarterly Results Extraction & QoQ/YoY Comparisons
print("\n[4. Quarterly Results Extraction & QoQ/YoY Comparisons]:")
for t in ['TRENT', 'DIXON']:
    with urllib.request.urlopen(f"{base_url}/results/{t}") as resp:
        qr = json.loads(resp.read().decode('utf-8'))
        cur = qr['current_quarter']
        prev_q = qr.get('previous_quarter')
        prev_y = qr.get('previous_year_quarter')
        print(f"Company: {qr['company_name']} ({qr['ticker']})")
        print(f"  Headline Takeaway: {qr['headline_takeaway']}")
        print(f"  Current Quarter ({cur['period']}): Rev=Rs {cur['revenue_cr']} Cr, EBITDA=Rs {cur['ebitda_cr']} Cr ({cur['ebitda_margin_pct']}% margin), PAT=Rs {cur['pat_cr']} Cr")
        print(f"  Growth: QoQ Rev={cur.get('revenue_qoq_pct')}%, YoY Rev={cur.get('revenue_yoy_pct')}%, YoY PAT={cur.get('pat_yoy_pct')}%")
        if prev_q:
            print(f"  Previous Quarter ({prev_q['period']}): Rev=Rs {prev_q['revenue_cr']} Cr, PAT=Rs {prev_q['pat_cr']} Cr")
        if prev_y:
            print(f"  Previous Year Qtr ({prev_y['period']}): Rev=Rs {prev_y['revenue_cr']} Cr, PAT=Rs {prev_y['pat_cr']} Cr")
        print(f"  Citations: {len(cur.get('citations', []))} citation items")
        for c in cur.get('citations', []):
            print(f"    - Source: {c['source_doc']} (Page {c['page_number']}) -> '{c['quote_snippet']}'")

print("\nSECTION 5 AUDIT COMPLETED.")
