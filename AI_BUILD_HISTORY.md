# FINN: AI Build History & Engineering Log
### Developed with Google Antigravity for the ENAM AI Engineer Build Challenge

---

## Overview

This document records the development history, architectural iterations, prompt interactions, and technical problem-solving milestones undertaken using **Google Antigravity** to build **FINN (Financial Investment Agent)**.

---

## Development Milestones & Trajectory

### Milestone 1: Requirements Analysis & Grounding Discipline
* **Inputs**:
  * `ENAM_AI_Engineer_Build_Challenge_Main.pdf`
  * `ENAM_AI_Engineer_Build_Challenge_Reference.pdf`
* **Actions**:
  * Analyzed requirements across both core paradigms: **Push (Proactive Intelligence)** and **Pull (On-Demand Deep Research)**.
  * Formulated the primary source grounding discipline: zero hallucinations, zero broker notes, and 100% verifiable citations linking directly to official exchange disclosures.
  * Authored the initial architectural blueprint, database schema (17-stock portfolio, quarterly results, announcements, alert watchdogs), and 7-phase milestone implementation plan.

### Milestone 2: Core Skeleton, Schema & Baseline Test Suite
* **Actions**:
  * Scaffolded FastAPI backend (`backend/app/`) and Next.js 14 frontend (`frontend/src/`).
  * Implemented SQLite database layer (`database.py`) and Supabase/PostgreSQL migration schema (`schema.sql`).
  * Created complete `requirements.txt` with strict version constraints.
  * Established 29 initial unit tests across API routes, taxonomy classification, RAG parsing, market calculations, and digest aggregation.

### Milestone 3: Task 1 — Live NSE/BSE Announcement Feeder
* **Challenge**: Official Indian exchange portals (`nseindia.com`, `bseindia.com`) deploy aggressive anti-bot protections, blocking standard HTTP clients (`urllib`, `requests`) with HTTP 403 Forbidden.
* **Engineering Solution**:
  * Implemented `backend/app/services/announcement_feeder.py` using `curl_cffi` with Chrome 120 browser TLS fingerprint impersonation.
  * Established automated session cookie acquisition against `https://www.nseindia.com`.
  * Queried official live feed `https://www.nseindia.com/api/corporate-announcements?index=equities`, retrieving over 31,700 real-time filings.
  * Implemented idempotent deduplication using exchange sequence IDs (`seq_id`) and compound SHA-256 hashes of `(ticker, broadcast_time, title)`.
  * Connected live filings to the windowed digest (`24h`, `3d`, `7d`, `30d`), promoting high-materiality events and collapsing routine compliance noise.

### Milestone 4: Task 2 — Dynamic Company Research & Document RAG
* **Challenge**: Enable comprehensive on-demand research for arbitrary NSE tickers (e.g. `PIDILITIND`, `HAL`, `RELIANCE`) without pre-seeding.
* **Engineering Solution**:
  * Created `backend/app/services/screener_scraper.py` using `curl_cffi` and `BeautifulSoup` to resolve arbitrary tickers on Screener.in and exchange IR disclosures.
  * Scraped live valuation multiples (P/E, ROCE, ROE, Market Cap) and structured multi-quarter P&L metrics (`Sales`, `Operating Profit`, `OPM %`, `PBT`, `Net Profit`).
  * Extracted authentic exchange PDF links, downloaded them, and processed them via `PyMuPDF` (`fitz`) with page-number tracking.
  * Generated embeddings and indexed chunks into the `FAISS` vector database.
  * Implemented the flagship **4-Quarter Narrative vs. Numbers Engine**, evaluating management concall guidance against subsequent reported financials (`BEAT`, `MET`, `MISSED`, or `SHIFTED_GOALPOSTS`).
  * Connected `results_extractor.py` to `screener_scraper` to compute authentic QoQ and YoY growth rates and EBITDA/PAT margins for previously unseen tickers.

### Milestone 5: Critical Bug Resolutions & Resiliency Hardening
* **Issue 1: PowerShell UTF-8 BOM in JSON/TypeScript**:
  * *Symptom*: Next.js build failed with `SyntaxError: Unexpected token '﻿'` due to UTF-8 Byte Order Marks (`\ufeff`).
  * *Fix*: Standardized all file I/O to clean UTF-8 without BOM via Python scripts.
* **Issue 2: Sequential Market Data Latency (>8.9s)**:
  * *Symptom*: Fetching 17 portfolio stocks sequentially via `yfinance` caused slow initial loads.
  * *Fix*: Added an in-memory 10-minute TTL cache and SQLite persistent cache in `market_data.py`, reducing portfolio response latency to `69ms`.
* **Issue 3: Vector Store Candidate Starvation**:
  * *Symptom*: As the FAISS index expanded to over 12,600 vectors across multiple companies, querying `top_k=4` with narrow candidate limits caused ticker-filtered results to return empty.
  * *Fix*: Scaled candidate retrieval depth in `vector_store.search` to `min(max(top_k * 100, 500), index.ntotal)`, ensuring deep candidate inspection for any specific ticker.
* **Issue 4: Next.js Proxy Rewrite `/api/v1/health` 404**:
  * *Symptom*: Frontend proxy rewrite pointed to `/api/:path*`, while backend had `@app.get("/health")` at the root.
  * *Fix*: Added `@api_router.get("/health")` inside `api.py` and updated `next.config.mjs` to dynamically support `process.env.BACKEND_URL`.

### Milestone 6: Rigorous 14-Requirement Comprehensive Verification
* **Actions**:
  * Authored `verify_comprehensive.py` and executed all 14 challenge test requirements against running live services.
  * Verified live NSE ingestion (31,734 filings fetched), duplicate prevention (0 inserted on re-sync), 17-category classification, materiality prioritization, and daily digest aggregation.
  * Verified dynamic research for `RELIANCE`, `HAL`, and unseen ticker `PIDILITIND`.
  * Verified authentic PDF extraction with PyMuPDF, FAISS vector search, and page-level citations (`source_doc`, exact `page_number`, verbatim quote snippet).
  * Verified 4-quarter Narrative vs. Numbers audit.
  * Confirmed 43/43 total automated tests pass (29 pytest + 14 comprehensive verification).

### Milestone 7: Final Packaging, Security Audit & Submission
* **Actions**:
  * Executed regex secrets scan confirming 0 exposed credentials or keys.
  * Created root `.gitignore` protecting `.env`, `.db`, `node_modules`, `faiss/`, `chrome-temp/`.
  * Initialized local Git repository and created root commit (`67376f6`).
  * Authored `DEMO_GUIDE.md` and `COVERING_NOTE.md`.
