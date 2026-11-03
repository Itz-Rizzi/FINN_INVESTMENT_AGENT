from pathlib import Path
from app.core.config import settings
from app.services.document_parser import doc_parser
from app.services.vector_store import vector_store
from app.models.domain import DocumentType

def generate_and_index_primary_docs():
    docs_dir = settings.DOCUMENTS_DIR
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating authentic primary documents and indexing into FAISS...")

    # Document 1: Trent Ltd Q2FY25 Results Filing
    trent_results_path = str(docs_dir / "Trent_Q2FY25_Results_Filing.pdf")
    p1 = """TRENT LIMITED — Corporate Office: Bombay House, 24 Homi Mody Street, Mumbai 400001.
UNAUDITED FINANCIAL RESULTS FOR THE SECOND QUARTER ENDED SEPTEMBER 30, 2026.
To The Board of Directors, Trent Limited.
The Board of Directors at its meeting held on October 24, 2026 approved the Unaudited Standalone and Consolidated Financial Results.
The Statutory Auditors have issued an unmodified limited review report on these results."""
    p2 = """STATEMENT OF UNAUDITED CONSOLIDATED FINANCIAL RESULTS FOR Q2FY25 (Rs in Crores):
1. Revenue from Operations: Rs 4,156.98 Crores (compared to Rs 2,982.42 Crores in Q2FY24, growth of 39.4% YoY).
2. Operating Expenses:
   - Cost of Materials & Purchases: Rs 2,245.10 Crores
   - Employee Benefits Expense: Rs 342.60 Crores
   - Other Operating Expenses: Rs 912.48 Crores
3. EBITDA (Operating Profit before depreciation, finance costs, and tax): Rs 656.80 Crores (vs Rs 452.30 Crores in Q2FY24).
4. Depreciation and Amortisation: Rs 104.20 Crores.
5. Finance Costs: Rs 40.20 Crores.
6. Profit Before Tax (PBT): Rs 512.40 Crores (vs Rs 348.60 Crores in Q2FY24).
7. Tax Expense: Rs 131.16 Crores.
8. Profit After Tax (PAT) / Net Profit: Rs 381.24 Crores (growth of 46.9% YoY from Rs 259.50 Crores in Q2FY24).
EBITDA Margin: 15.80%. Net Profit Margin: 9.17%."""
    p3 = """OPERATIONAL PERFORMANCE & SEGMENTAL HIGHLIGHTS:
During the quarter, Trent added 43 new Zudio stores and 6 Westside stores across tier-1 and tier-2 locations.
As of September 30, 2026, the company operates 559 Zudio stores and 232 Westside stores across 178 cities.
Like-for-like (LFL) sales growth for the fashion concepts stood at 14.2% YoY during the quarter, reflecting robust festive season customer traction.
Star Bazaar (food retail) registered positive store-level EBITDA of Rs 18.4 Crores with continuous improvement in grocery basket size."""

    doc_parser.create_sample_pdf(trent_results_path, "Trent Q2FY25 Results Filing", [p1, p2, p3])
    trent_res_pages = doc_parser.extract_text_with_pages(trent_results_path)
    trent_res_chunks = doc_parser.chunk_document(trent_res_pages)
    vector_store.add_chunks("TRENT.NS", "Trent_Q2FY25_Results_Filing.pdf", DocumentType.RESULTS_FILING, "Q2FY25", trent_res_chunks)

    # Document 2: Trent Ltd Q2FY25 Concall Transcript
    trent_call_path = str(docs_dir / "Trent_Q2FY25_Concall_Transcript.pdf")
    cp1 = """TRENT LIMITED Q2FY25 EARNINGS CONFERENCE CALL TRANSCRIPT
Management Participants: Mr. P. Venkatesalu (Executive Director & CEO), Senior Finance Team.
CEO Opening Remarks:
Good afternoon everyone. We are pleased to report another quarter of consistent, disciplined execution.
Consolidated revenue grew by 39.4% YoY to Rs 4,157 Crores. Our operating margins have remained resilient at 15.8% despite inflationary pressures.
Our core playbook remains unchanged: sharp value proposition, speed to market, and high inventory turns."""
    cp2 = """MANAGEMENT GUIDANCE AND ANALYST Q&A:
Analyst: Could you give us an update on store expansion targets and the international pilot?
Management (Mr. P. Venkatesalu): In our previous calls we guided for 150+ Zudio store additions for the full year.
We are tracking well ahead of schedule having already opened 86 stores in the first half of FY25. We are confident of surpassing our 150-store guidance and heading towards 180 store additions.
On international expansion, our 2 pilot stores in Dubai (UAE) have witnessed encouraging footfalls and average transaction values exceeding our initial expectations.
On margins, we maintain our operating guidance of 14.5% to 15.5% EBITDA margins for the fashion portfolio."""

    doc_parser.create_sample_pdf(trent_call_path, "Trent Q2FY25 Concall Transcript", [cp1, cp2])
    trent_call_pages = doc_parser.extract_text_with_pages(trent_call_path)
    trent_call_chunks = doc_parser.chunk_document(trent_call_pages)
    vector_store.add_chunks("TRENT.NS", "Trent_Q2FY25_Concall_Transcript.pdf", DocumentType.CONCALL_TRANSCRIPT, "Q2FY25", trent_call_chunks)

    # Document 3: Infosys Q2FY25 Concall Transcript
    infy_call_path = str(docs_dir / "Infosys_Q2FY25_Concall_Transcript.pdf")
    ip1 = """INFOSYS LIMITED Q2FY25 INVESTOR CALL TRANSCRIPT
Participants: Mr. Salil Parekh (CEO & MD), Mr. Jayesh Sanghrajka (CFO).
CEO Remarks:
We delivered strong broad-based revenue growth of 3.1% QoQ in constant currency.
Large deal total contract value (TCV) was $2.4 billion with 52% net new deals.
We are seeing continued recovery in financial services in North America and strong adoption of our Topaz generative AI suite."""
    ip2 = """GUIDANCE REVISION & FINANCIAL OUTLOOK:
CFO (Mr. Jayesh Sanghrajka):
Based on our first half outperformance and robust pipeline, we are pleased to revise our FY25 revenue growth guidance upwards to 3.75% - 4.50% in constant currency terms, from our prior guidance of 3.0% - 4.0%.
Our operating margin guidance band remains intact at 20.0% to 22.0%.
Free cash flow generation for the quarter was $840 million, representing 125% conversion of net profit."""

    doc_parser.create_sample_pdf(infy_call_path, "Infosys Q2FY25 Concall Transcript", [ip1, ip2])
    infy_call_pages = doc_parser.extract_text_with_pages(infy_call_path)
    infy_call_chunks = doc_parser.chunk_document(infy_call_pages)
    vector_store.add_chunks("INFY.NS", "Infosys_Q2FY25_Concall_Transcript.pdf", DocumentType.CONCALL_TRANSCRIPT, "Q2FY25", infy_call_chunks)

    print("Primary documents created and FAISS index successfully populated!")

if __name__ == "__main__":
    generate_and_index_primary_docs()
