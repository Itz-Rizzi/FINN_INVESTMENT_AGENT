import pymupdf
import re
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

from app.core.config import settings
from app.models.domain import DocumentType

logger = logging.getLogger(__name__)

class DocumentParserService:
    @staticmethod
    def extract_text_with_pages(pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extracts text from PDF page by page using PyMuPDF.
        Returns a list of dicts: [{"page_number": int, "text": str}]
        """
        pages_content = []
        try:
            doc = pymupdf.open(pdf_path)
            for page_idx in range(len(doc)):
                page = doc[page_idx]
                text = page.get_text("text")
                # Clean excessive whitespace
                cleaned_text = re.sub(r"\n{3,}", "\n\n", text).strip()
                if cleaned_text:
                    pages_content.append({
                        "page_number": page_idx + 1,
                        "text": cleaned_text
                    })
            doc.close()
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
        return pages_content

    @classmethod
    def chunk_document(
        cls, 
        pages_content: List[Dict[str, Any]], 
        chunk_size: int = 500, 
        overlap: int = 80
    ) -> List[Dict[str, Any]]:
        """
        Chunks text while strictly preserving page number metadata.
        """
        chunks = []
        chunk_idx = 0
        
        for item in pages_content:
            page_num = item["page_number"]
            words = item["text"].split()
            
            if not words:
                continue

            i = 0
            while i < len(words):
                chunk_words = words[i:i + chunk_size]
                chunk_text = " ".join(chunk_words)
                
                chunks.append({
                    "chunk_index": chunk_idx,
                    "page_number": page_num,
                    "text": chunk_text
                })
                chunk_idx += 1
                i += (chunk_size - overlap)
                if i >= len(words):
                    break

        return chunks

    @classmethod
    def create_sample_pdf(cls, output_path: str, title: str, pages_data: List[str]):
        """
        Generates an authentic PDF using PyMuPDF for testing and guaranteed offline evaluation.
        """
        doc = pymupdf.open()
        for idx, text in enumerate(pages_data):
            page = doc.new_page(width=595, height=842) # A4 size
            # Insert header
            page.insert_text((50, 40), f"{title} — Page {idx+1}", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
            # Insert body
            rect = pymupdf.Rect(50, 70, 545, 800)
            page.insert_textbox(rect, text, fontsize=10, fontname="helv", color=(0, 0, 0))
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path)
        doc.close()
        return output_path

doc_parser = DocumentParserService()
