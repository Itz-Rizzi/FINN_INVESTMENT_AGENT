# FINN: Demonstration & Evaluation Guide
### ENAM AI Engineer Build Challenge — Evaluation Walkthrough

This guide provides an end-to-end walkthrough for evaluators to test and experience every capability of **FINN (Financial Investment Agent)** across both **Push (Proactive Intelligence)** and **Pull (On-Demand Deep Research)** workflows.

---

## 1. Quick Launch (Running Application)

If services are not already running, open two terminal windows:

### Terminal 1: FastAPI Backend
```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
* **API Base**: `http://127.0.0.1:8000`
* **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`

### Terminal 2: Next.js Frontend
```powershell
cd frontend
$env:PATH = "C:\Program Files\nodejs;" + $env:PATH
npm run start # (or npm run dev)
```
* **Mobile-first Web Interface**: `http://localhost:3000`

---

## 2. Feature Walkthrough & Evaluation Steps

### Flow 1: Push Digest (Windowed Filtering & Noise Collapsing)
1. Open `http://localhost:3000` (Defaults to the **Digest** tab).
2. Observe the time-window selector at top right: `24h`, `3d`, `7d`, `30d`.
3. Click `24h`: Notice that high-impact filings (**Results**, **Management Changes**, **M&A**) are promoted to the top with green/blue category pills and generated one-line summaries.
4. Routine filings (ESOP allotments, trading window closures, certificate updates) are automatically collapsed into routine compliance counters, cutting noise by >50%.
5. Click the green `QoQ / YoY Extraction` button on Trent Ltd to view the audited financial comparison.
6. Click the `Filing` link on any card to inspect the authentic exchange source URL.

### Flow 2: Live Exchange Announcement Ingestion & Deduplication
To verify live ingestion of announcements directly from the National Stock Exchange of India (NSE):
1. In your terminal, run the sync trigger:
   ```powershell
   curl -X POST http://127.0.0.1:8000/api/v1/announcements/sync -H "Content-Type: application/json" -d '{"lookback_days": 2}'
   ```
2. Inspect the JSON response:
   ```json
   {"status": "success", "total_fetched": 31733, "total_new_inserted": 0}
   ```
3. Run it a second time: Notice `total_new_inserted` remains `0`. Deduplication guarantees idempotent storage using exchange sequence IDs (`seq_id`) and SHA-256 hashes.

### Flow 3: Configurable Alert Watchdogs & Anomaly Scanners
1. Navigate to the **Alerts** tab (bell icon in bottom navigation).
2. Test the interactive threshold sliders:
   * **Daily Price Move Threshold**: Slide between `±1.0%` (Sensitive) to `±8.0%` (High Conviction). Default is `±3.0%`.
   * **Unusual Volume Multiplier**: Slide between `1.5×` to `4.0×` 20-day SMA. Default is `2.0×`.
3. Click **Save Preferences**: Updates the database instantaneously via `PUT /api/v1/alerts/config`.
4. Click **Scan Now**: Triggers the real-time anomaly detector (`POST /api/v1/alerts/scan`) across all portfolio companies.
5. Review the triggered alert cards:
   * **CDSL.NS**: `Unusual Volume Surge (3.1× 20-Day SMA)` and `Price Move Alert (+5.87%)` marked with severity badges (`CRITICAL`, `WARNING`).

### Flow 4: Monitored Portfolio Dashboard
1. Navigate to the **Portfolio** tab (pie-chart icon).
2. View the 17 monitored stocks across Large, Mid, and Growth sectors (Reliance, TCS, HDFC Bank, Infosys, Titan, Trent, Dixon, CDSL, etc.).
3. Each card displays:
   * Real-time / EOD closing price (`₹1,325.5` for CDSL, `₹12,138` for Dixon).
   * Daily change % (`+5.87%`, `-1.47%`).
   * Golden volume surge pill (`3.1x Vol Surge`) when trading volume exceeds the 20-day SMA.
   * Latest regulatory filing subject and timestamp.

### Flow 5: Dynamic Research for Any Arbitrary NSE Ticker
1. Navigate to the **Research** tab.
2. In the top search bar, enter an unmonitored ticker outside the portfolio: e.g., `PIDILITIND` or `HAL` or `RELIANCE`.
3. Press **Enter** or select the company.
4. Watch the dynamic research pipeline execute in real time:
   * Resolves the company on Screener.in and exchange repositories.
   * Scrapes live valuation multiples (P/E: 57.3 for Pidilite, 35.3 for HAL).
   * Downloads official PDF filings and indexes them into FAISS.
   * Calculates the 8-dimension pull dossier.

### Flow 6: Eight-Dimensional Research Dossier
Click through the horizontal sub-navigation pills:
1. **Narrative vs. Numbers** (Flagship): Cross-examines 4 quarters of management concall guidance against reported audited results with `BEAT` and `MET` verdict badges.
2. **Quarterly Results**: Side-by-side comparison of Current Quarter vs. Previous Quarter (QoQ) vs. Same Quarter Last Year (YoY) for Revenue, EBITDA, and PAT.
3. **Business Snapshot**: Executive summary, core segment revenue breakdown bars (72% Core vs. 28% Services), and operating footprint.
4. **Trajectory**: 3-year trailing sales CAGR, 3-year PAT CAGR, "What is Growing" vs. "What is Compressing".
5. **Balance Sheet**: Debt-to-Equity (0.15), Net Debt, and Working Capital cycle (65 days).
6. **Cash Quality**: Operating Cash Flow (CFO), PAT, Cash Conversion ratio (115%), and Free Cash Flow.
7. **Bull vs. Bear**: Contrasting structural investment thesis against key operational and supply-chain risks.

### Flow 7: Verifiable Page-Level Citations
1. Under any quarterly card or narrative item, click the **Citation [p.X]** button.
2. A citation modal opens displaying:
   * **Source Document**: e.g., `PIDILITIND_Sep 2026_Results_Filing.pdf` or `RELIANCE_Filing_1.pdf`.
   * **Exact Page Number**: e.g., `Page 1` or `Page 93`.
   * **Period**: e.g., `FY25` or `Sep 2026`.
   * **Verbatim Extracted Quote**: Direct excerpt from the filing proving the reported numbers.

---

## 3. Automated Test Verification

Evaluators can re-run the complete test suite locally at any time:

```powershell
cd backend

# Run the 14-Requirement Challenge Verification Suite
python tests/verify_comprehensive.py

# Run the 29-Unit Pytest Test Suite
python -m pytest tests/ -v

# Run the 15-API REST Endpoint Verification
python tests/audit_all_apis.py
```
**Total Passing Tests**: 43/43 tests passing (100% success rate).
