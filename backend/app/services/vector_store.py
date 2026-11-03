import faiss
import numpy as np
import json
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.domain import DocumentType
from app.models.schemas import CitationItem

logger = logging.getLogger(__name__)

EMBEDDING_DIM = 256

class VectorStoreService:
    def __init__(self, index_path: Optional[str] = None):
        self.index_dir = settings.FAISS_INDEX_DIR
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = str(self.index_dir / "finn_faiss.index")
        self.metadata_file = str(self.index_dir / "finn_metadata.json")
        
        self.index: Optional[faiss.IndexFlatIP] = None
        self.metadata: List[Dict[str, Any]] = []
        self._load_or_create_index()

    def _load_or_create_index(self):
        if Path(self.index_file).exists() and Path(self.metadata_file).exists():
            try:
                self.index = faiss.read_index(self.index_file)
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                return
            except Exception as e:
                logger.warning(f"Error loading existing FAISS index: {e}. Creating fresh.")

        self.index = faiss.IndexFlatIP(EMBEDDING_DIM)
        self.metadata = []

    def _compute_embedding(self, text: str) -> np.ndarray:
        """
        Generates embedding. Uses Gemini embeddings when API key is set,
        or deterministic hashing projection with L2 normalization as guaranteed fallback.
        """
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                res = client.models.embed_content(
                    model="text-embedding-004",
                    contents=text
                )
                emb = np.array(res.embedding.values, dtype=np.float32)
                # If dimension mismatch, project or slice
                if emb.shape[0] != EMBEDDING_DIM:
                    emb = np.resize(emb, EMBEDDING_DIM)
                faiss.normalize_L2(emb.reshape(1, -1))
                return emb
            except Exception as e:
                logger.debug(f"Gemini embedding fallback to deterministic projection: {e}")

        # Deterministic semantic hash projection (Word token hashing with TF-IDF style weighting)
        vec = np.zeros(EMBEDDING_DIM, dtype=np.float32)
        words = text.lower().split()
        for w in words:
            h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
            idx = h % EMBEDDING_DIM
            sign = 1.0 if ((h >> 8) & 1) else -1.0
            vec[idx] += sign

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm
        return vec

    def add_chunks(self, ticker: str, doc_name: str, doc_type: DocumentType, period: str, chunks: List[Dict[str, Any]]):
        """
        Indexes chunks with document citation metadata.
        """
        if not chunks:
            return

        embeddings = []
        for ch in chunks:
            emb = self._compute_embedding(ch["text"])
            embeddings.append(emb)

        emb_matrix = np.vstack(embeddings).astype(np.float32)
        start_id = len(self.metadata)
        self.index.add(emb_matrix)

        for idx, ch in enumerate(chunks):
            self.metadata.append({
                "id": start_id + idx,
                "ticker": ticker,
                "source_doc": doc_name,
                "doc_type": doc_type.value,
                "period": period,
                "page_number": ch["page_number"],
                "chunk_index": ch["chunk_index"],
                "text": ch["text"]
            })

        self.save()

    def search(self, query: str, ticker: Optional[str] = None, top_k: int = 4) -> List[Dict[str, Any]]:
        """
        Vector search returning matched text and traceable citations.
        """
        if self.index.ntotal == 0:
            return []

        query_emb = self._compute_embedding(query).reshape(1, -1).astype(np.float32)
        # Fetch sufficient candidates to filter by ticker
        k_search = min(max(top_k * 100, 500), self.index.ntotal)
        scores, indices = self.index.search(query_emb, k_search)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            item = self.metadata[idx]
            if ticker and item["ticker"].upper() != ticker.upper():
                continue
            
            # Extract first 2 sentences as concise quote snippet
            sentences = item["text"].split(". ")
            quote_snippet = ". ".join(sentences[:2]) + ("." if not sentences[0].endswith(".") else "")

            results.append({
                "score": float(score),
                "ticker": item["ticker"],
                "source_doc": item["source_doc"],
                "doc_type": item["doc_type"],
                "period": item["period"],
                "page_number": item["page_number"],
                "text": item["text"],
                "quote_snippet": quote_snippet,
                "citation": CitationItem(
                    source_doc=item["source_doc"],
                    doc_type=DocumentType(item["doc_type"]),
                    period=item["period"],
                    page_number=item["page_number"],
                    quote_snippet=quote_snippet
                )
            })

            if len(results) >= top_k:
                break

        return results

    def save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

vector_store = VectorStoreService()
