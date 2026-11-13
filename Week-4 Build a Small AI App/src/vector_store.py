"""
Vector Store and Semantic Search Engine.
Converts text chunks into embeddings via Gemini API, computes cosine similarity,
and caches vectors locally for fast, repeatable retrieval.
"""

import os
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
        # Try current dir and parent dir for .env
        load_dotenv()
        load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
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

        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["embedding"]["values"]

    def add_chunks(self, chunks: List[Dict[str, Any]], batch_size: int = 20) -> None:
        """
        Embeds multiple text chunks using batchEmbedContents and stores them.
        """
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-embedding-001:batchEmbedContents?key={self.api_key}"
        )

        total = len(chunks)
        print(f"Embedding {total} chunks in batches of {batch_size}...")

        for i in range(0, total, batch_size):
            batch = chunks[i:i + batch_size]
            requests = [
                {
                    "model": "models/gemini-embedding-001",
                    "content": {"parts": [{"text": c["text"][:2000]}]}
                }
                for c in batch
            ]
            data = json.dumps({"requests": requests}).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

            try:
                with urllib.request.urlopen(req) as resp:
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
                print(f"  Processed {min(i + batch_size, total)}/{total} chunks...")
                time.sleep(0.5)  # Respect free API rate limits
            except urllib.error.HTTPError as e:
                print(f"  [Warning] HTTP Error {e.code}: {e.reason}. Retrying batch...")
                time.sleep(2)

    def save_cache(self, file_path: str) -> None:
        """Saves stored vectors and metadata to disk."""
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.entries, f)
        print(f"[OK] Cached {len(self.entries)} vector entries to: {file_path}")

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
        Searches the stored chunks and returns the top-k most semantically relevant.
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
    # Self-test block: Embed a sample of chunks and run a test query
    print("=== Testing Vector Store & Semantic Search ===")
    
    # Locate cache directory
    script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else "."
    cache_path = os.path.join(script_dir, "vector_cache", "sample_embeddings.json")
    
    store = SimpleVectorStore()
    
    # Try loading existing cache first
    if not store.load_cache(cache_path):
        print("No cache found. Simulating with 3 distinct test chunks...")
        sample_chunks = [
            {
                "chunk_id": "chunk_academic_1",
                "page_number": 42,
                "source": "AASTU Handbook",
                "text": "Academic Standing: A student must maintain a minimum Cumulative Grade Point Average (CGPA) of 2.00 to remain in good standing. Failure to do so leads to academic probation."
            },
            {
                "chunk_id": "chunk_library_1",
                "page_number": 88,
                "source": "AASTU Handbook",
                "text": "Library Services: The university library opens at 8:00 AM and closes at 10:00 PM on weekdays. Valid student ID card is mandatory for entry."
            },
            {
                "chunk_id": "chunk_sports_1",
                "page_number": 115,
                "source": "AASTU Handbook",
                "text": "Campus Recreation: The university gymnasium and sports fields are open for all registered undergraduate students during scheduled athletic hours."
            }
        ]
        store.add_chunks(sample_chunks, batch_size=10)
        store.save_cache(cache_path)

    # Test Query: Student asking about minimum CGPA
    test_query = "What is the minimum CGPA required for good academic standing?"
    print(f"\nQuery: '{test_query}'")
    results = store.search(test_query, top_k=2)

    print("\n--- Search Results (Top Matches) ---")
    for rank, r in enumerate(results, 1):
        print(f"\n#{rank} [Score: {r['similarity_score']}] (Page {r['page_number']})")
        print(f"Excerpt: {r['text'][:140]}...")