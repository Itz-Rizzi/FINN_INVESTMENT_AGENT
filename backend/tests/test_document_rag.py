import pytest
from app.services.document_parser import doc_parser
from app.services.vector_store import vector_store
from app.core.config import settings
from app.models.domain import DocumentType

def test_document_extraction():
    test_pdf = str(settings.DOCUMENTS_DIR / "Trent_Q2FY25_Results_Filing.pdf")
    pages = doc_parser.extract_text_with_pages(test_pdf)
    assert len(pages) >= 2
    assert pages[0]["page_number"] == 1
    assert "TRENT" in pages[0]["text"].upper()
    assert pages[1]["page_number"] == 2
    assert "REVENUE" in pages[1]["text"].upper()

def test_chunking_with_page_preservation():
    sample_pages = [
        {"page_number": 1, "text": "This is page one text with financial overview. " * 30},
        {"page_number": 2, "text": "This is page two text discussing balance sheet. " * 30}
    ]
    chunks = doc_parser.chunk_document(sample_pages, chunk_size=50, overlap=10)
    assert len(chunks) > 0
    # Every chunk must have a valid page number
    for ch in chunks:
        assert ch["page_number"] in [1, 2]
        assert len(ch["text"]) > 0

def test_faiss_vector_retrieval_with_citations():
    # Query for Zudio stores in Trent filings
    results = vector_store.search("Zudio store additions and expansion", ticker="TRENT.NS", top_k=2)
    assert len(results) > 0
    top = results[0]
    assert top["ticker"] == "TRENT.NS"
    assert "citation" in top
    assert top["citation"].page_number in [2, 3]
    assert top["citation"].source_doc.endswith(".pdf")
    assert len(top["quote_snippet"]) > 10

def test_faiss_guidance_query():
    # Query for Infosys revenue growth guidance
    results = vector_store.search("revenue growth guidance revision", ticker="INFY.NS", top_k=1)
    assert len(results) > 0
    top = results[0]
    assert top["ticker"] == "INFY.NS"
    assert "3.75%" in top["text"] or "guidance" in top["text"].lower()
