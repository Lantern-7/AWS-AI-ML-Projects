"""
Vector Store and Semantic Search Engine.
Converts text chunks into embeddings via Gemini API, computes cosine similarity,
and caches vectors locally for fast, repeatable retrieval.
"""

import os
import sys
import math
import json
import time
import urllib.request
import urllib.error
from typing import List, Dict, Any


def get_gemini_api_key() -> str:
    """
    Safely retrieves the Gemini API key from Google Colab Secrets
    or local .env / environment variables.
    """
    # 1. Try Google Colab userdata
    try:
        from google.colab import userdata
        key = userdata.get("GEMINI_API_KEY")
        if key:
            return key
    except Exception:
        pass

    # 2. Try python-dotenv for local development
    try:
        from dotenv import load_dotenv
        load_dotenv()
        script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else "."
        load_dotenv(os.path.join(script_dir, "..", ".env"))
        load_dotenv(os.path.join(script_dir, ".env"))
    except Exception:
        pass

    key = os.getenv("GEMINI_API_KEY")
    if not key or key.startswith("your_"):
        raise ValueError(
            "GEMINI_API_KEY not found! Please set it in your .env file or Colab Secrets (🔑)."
        )
    return key


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Computes the cosine similarity between two numeric vectors."""
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    if norm_v1 == 0.0 or norm_v2 == 0.0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)


class SimpleVectorStore:
    """A lightweight vector store with batch embedding and disk caching."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or get_gemini_api_key()
        self.entries: List[Dict[str, Any]] = []

    def get_embedding(self, text: str) -> List[float]:
        """Embeds a single query string using gemini-embedding-001."""
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-embedding-001:embedContent?key={self.api_key}"
        )
        payload = {
            "model": "models/gemini-embedding-001",
            "content": {"parts": [{"text": text[:2000]}]}
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["embedding"]["values"]

    def add_chunks(self, chunks: List[Dict[str, Any]], batch_size: int = 25, cache_path: str = None) -> None:
        """
        Embeds multiple text chunks using batchEmbedContents with automated
        network retry and incremental progress saving.
        """
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-embedding-001:batchEmbedContents?key={self.api_key}"
        )

        # Check existing chunks to resume if interrupted
        existing_ids = {e["chunk_id"] for e in self.entries}
        remaining_chunks = [c for c in chunks if c["chunk_id"] not in existing_ids]

        total = len(chunks)
        start_idx = total - len(remaining_chunks)

        if start_idx > 0:
            print(f"Resuming from chunk {start_idx}/{total} (already in database)...")

        for i in range(0, len(remaining_chunks), batch_size):
            batch = remaining_chunks[i:i + batch_size]
            current_count = start_idx + i + len(batch)

            requests = [
                {
                    "model": "models/gemini-embedding-001",
                    "content": {"parts": [{"text": c["text"][:2000]}]}
                }
                for c in batch
            ]
            data = json.dumps({"requests": requests}).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

            # Retry loop: attempt up to 3 times per batch on network drops
            success = False
            for attempt in range(1, 4):
                try:
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        res = json.loads(resp.read().decode("utf-8"))
                        embeddings = res.get("embeddings", [])
                        for chunk, emb in zip(batch, embeddings):
                            self.entries.append({
                                "chunk_id": chunk["chunk_id"],
                                "page_number": chunk["page_number"],
                                "source": chunk.get("source", "AASTU Handbook"),
                                "text": chunk["text"],
                                "vector": emb["values"]
                            })
                    success = True
                    print(f"  Processed {current_count}/{total} chunks...")
                    break
                except Exception as e:
                    wait_time = 12 if "HTTPError" in str(type(e).__name__) else 4
                    print(f"  [Attempt {attempt}/3] Rate limit / network pause ({type(e).__name__}). Waiting {wait_time}s...")
                    time.sleep(wait_time)

            if not success:
                print(f"  [Error] Failed batch at chunk {current_count}. Saving current progress...")
                if cache_path:
                    self.save_cache(cache_path)
                raise RuntimeError(f"Network failed after 3 retries at chunk {current_count}")

            # Save checkpoint every 100 chunks
            if cache_path and (current_count % 100 == 0 or current_count == total):
                self.save_cache(cache_path)

            time.sleep(1.2)  # Respect free API rate limits

    def save_cache(self, file_path: str) -> None:
        """Saves stored vectors and metadata to disk."""
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.entries, f)
        print(f"[OK] Saved {len(self.entries)} vector entries to: {file_path}")

    def load_cache(self, file_path: str) -> bool:
        """Loads vectors from disk cache if the file exists."""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.entries = json.load(f)
            print(f"[OK] Loaded {len(self.entries)} vector entries from cache: {file_path}")
            return True
        return False

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Searches stored chunks and returns the top-k most semantically relevant.
        """
        if not self.entries:
            raise ValueError("Vector store is empty! Add chunks or load from cache first.")

        query_vec = self.get_embedding(query)
        scored_results = []

        for entry in self.entries:
            score = cosine_similarity(query_vec, entry["vector"])
            scored_results.append({
                "chunk_id": entry["chunk_id"],
                "page_number": entry["page_number"],
                "source": entry["source"],
                "text": entry["text"],
                "similarity_score": round(score, 4)
            })

        # Sort descending by similarity score
        scored_results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_results[:top_k]


if __name__ == "__main__":
    print("=== Testing Vector Store ===")
    store = SimpleVectorStore()
    print("Vector Store initialized successfully!")