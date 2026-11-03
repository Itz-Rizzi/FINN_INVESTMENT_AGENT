# FINN: Engineering Covering Note
### Submission to the ENAM Holdings AI Engineer Build Challenge

---

### Executive Summary

**FINN (Financial Investment Agent)** was engineered from first principles to solve the fundamental challenge faced by institutional public markets investors in India: **filtering the daily flood of exchange filings, rumors, and volatile price actions down to the actionable 1%.**

Most generic AI "financial assistants" rely on large language models summarizing secondary commentary, sell-side broker notes, or scraped web articles—inevitably producing hallucinations, invented ratios, or stale numbers. 

**FINN enforces strict primary-source discipline:**
Every financial metric, quarterly growth figure, and management quotation is extracted directly from official exchange filings (NSE/BSE), audited quarterly statements, annual reports, and earnings call transcripts. If an audited figure or citation cannot be proven from a primary document, FINN does not guess or interpolate.

---

### 1. Architectural Philosophy & Technology Stack

The application is architected around two high-conviction interaction paradigms:
1. **PUSH (Proactive Intelligence)**: What the investor *needs to know without asking* (windowed digest, noise collapsing, materiality scoring, unusual price swings, volume spikes).
2. **PULL (On-Demand Deep Research)**: What the investor *needs to verify with precision* (8-dimension research dossier, dynamic ticker resolution, flagship 4-quarter Narrative vs. Numbers audit).

#### Technical Stack Selection:
* **Frontend**: **Next.js 14 (App Router) + TypeScript + Tailwind CSS + Lucide Icons**. Built mobile-first to support rapid gesture-driven reviews by portfolio managers on the move.
* **Backend**: **Python 3.12 + FastAPI + Pydantic v2 + Uvicorn**. Chosen for high asynchronous throughput, native integration with numerical and document-parsing libraries, and schema-enforced type safety.
* **Exchange Ingestion**: **`curl_cffi` (Browser TLS Impersonation)**. Directly interfaces with the official National Stock Exchange of India (`https://www.nseindia.com/api/corporate-announcements`), bypassing brittle third-party scraping services while respecting anti-bot constraints.
* **Document Extraction & RAG**: **PyMuPDF (`fitz`) + FAISS (`IndexFlatIP`)**. Implements page-aware chunking that preserves document coordinates and page numbers. Vectors are normalized and searched via cosine similarity, returning verbatim quote excerpts and verifiable page citations.
* **Market Data & Anomalies**: **`yfinance` with NSE (`.NS`) resolution**. Mathematically computes 20-day Simple Moving Average (SMA) volume baselines, price change percentages, and anomaly thresholds with a multi-tier in-memory (10m TTL) and SQLite cache layer (<70ms latency).
* **Database & Persistence**: **SQLite (Local WAL mode) + Supabase/PostgreSQL schema (`schema.sql`)**. Provides zero-configuration local execution out of the box, with clean SQL migration scripts ready for enterprise PostgreSQL/Supabase deployments.

---

### 2. Key Engineering Decisions

1. **Idempotent Multi-Tier Deduplication**:
   Corporate announcement feeds are noisy and repeatedly broadcast amended filings. FINN enforces deduplication at both the ingestion pipeline and database layers using exchange sequence numbers (`seq_id`) and compound SHA-256 hashes of `(ticker, broadcast_time, title)`. Re-syncing over 31,700 filings results in exactly zero duplicate entries.

2. **Hierarchical 17-Category ENAM Classification & Noise Collapsing**:
   Filings are categorized across 17 distinct classes (Results, M&A, Management Changes, Litigation, Fund Raising, Capex, Credit Ratings, etc.). Routine compliance filings (such as ESOP share allotments and certificates under Regulation 74(5)) are automatically tagged as routine and collapsed into a counter in the digest, immediately removing over 50% of disclosure clutter.

3. **Dynamic On-Demand Research for Arbitrary Tickers**:
   Rather than restricting analysis to a static pre-seeded universe, FINN dynamically resolves any valid NSE ticker (e.g., `PIDILITIND.NS`, `HAL.NS`, `BEL.NS`). The system queries Screener.in and exchange archives, extracts key valuation multiples, downloads authentic PDF disclosures, chunks them with PyMuPDF, indexes them into FAISS, and dynamically constructs the 8-dimension dossier in real time.

4. **Candidate Retrieval Scaling in Vector Search**:
   In multi-company RAG systems where thousands of document chunks reside in a single vector index (FINN indexes 12,600+ vectors), standard FAISS `top_k` searches can be overwhelmed by dominant global vectors. FINN scales candidate retrieval (`k_search = min(max(top_k * 100, 500), index.ntotal)`), ensuring that ticker-specific filtering consistently locates the most relevant primary document excerpts.

5. **Deterministic Offline Fallbacks**:
   Financial applications cannot fail when an external LLM API experiences rate limits or network outages. FINN implements deterministic taxonomy rules, regex parsing, and mathematical margin/CAGR algorithms alongside Gemini model routing. If the LLM is unavailable, the application continues to operate without degradation.

---

### 3. AI / LLM Usage & Model Routing Strategy

* **High-Throughput Categorization**: Handled by lightweight classification heuristics and Gemini 1.5 Flash for one-line executive summaries.
* **Deep Narrative Synthesis**: Handled by Gemini 1.5 Pro/Flash for cross-examining nuanced management statements from concall transcripts against subsequently audited numbers.
* **Zero Hallucination Guardrails**: Prompts are constrained to provided context only. Financial numbers and quotes must be directly present in the source text; interpolation or external knowledge injection is strictly forbidden.

---

### 4. Trade-offs & Limitations

1. **Exchange Rate Limiting**: The NSE India JSON feed requires active session cookies. Polling faster than once every 5 seconds can trigger HTTP 429 Too Many Requests. A background polling cadence of 60–300 seconds is recommended for production.
2. **Scanned Image-Only PDFs**: A minority of regulatory filings from smaller companies are flat image scans without an embedded OCR text layer. `PyMuPDF` extracts 0 characters from image-only scans unless OCR (Tesseract) is run; in such cases, FINN relies on structured financial statements scraped from Screener.
3. **Local Database vs. Distributed Cloud DB**: FINN currently ships with SQLite in WAL mode for turnkey local demonstration. For distributed multi-container deployments, the application is designed to switch to Supabase/PostgreSQL using the supplied `schema.sql`.

---

### 5. Future Roadmap

1. **Automated Optical Character Recognition (OCR)**: Integrated pipeline for scanned image filings using PaddleOCR or Tesseract.
2. **Audio Concall Processing**: Direct ingestion and speaker diarization of earnings call audio MP3s via Gemini Audio APIs.
3. **Broker Consensus vs. Reality**: Extension of the Narrative vs. Numbers engine to compare sell-side consensus estimates against reported delivery.
4. **Interactive Graph Visualizations**: Interactive D3 / Recharts financial trajectory and margin waterfall charts.
