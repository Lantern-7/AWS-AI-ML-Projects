"""
Full Document Ingestion Pipeline for AASTU Handbook.
Generates embeddings for all 1,001 handbook chunks via Gemini API
and saves the complete vector database to disk.
"""

import os
import sys
import time

# Ensure src/ is discoverable
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from document_loader import load_pdf_pages, chunk_text, find_handbook_path
from vector_store import SimpleVectorStore


def build_full_handbook_index(batch_size: int = 25):
    print("=" * 65)
    print("   BUILDING COMPLETE AASTU HANDBOOK VECTOR DATABASE")
    print("=" * 65)

    # 1. Load the entire PDF
    pdf_path = find_handbook_path()
    print(f"Loading PDF from: {pdf_path}")
    pages = load_pdf_pages(pdf_path)
    print(f"[OK] Successfully loaded {len(pages)} pages.")

    # 2. Split into broad, 1000-character chunks
    chunks = chunk_text(pages, chunk_size=1000, chunk_overlap=200)
    total_chunks = len(chunks)
    print(f"[OK] Generated {total_chunks} broad searchable chunks.")

    # 3. Initialize Vector Store & load any existing progress
    store = SimpleVectorStore()
    cache_dir = os.path.join(script_dir, "vector_cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, "handbook_embeddings.json")

    # Resume from existing cache if partially built
    store.load_cache(cache_path)

    start_time = time.time()

    # 4. Ingest and embed all chunks (with incremental saving)
    store.add_chunks(chunks, batch_size=batch_size, cache_path=cache_path)

    # 5. Final save
    store.save_cache(cache_path)

    elapsed = time.time() - start_time
    print("\n" + "=" * 65)
    print(f"[SUCCESS] Ingestion complete in {elapsed:.1f} seconds!")
    print(f"Complete database saved to: {cache_path}")
    print(f"Total handbook chunks indexed: {len(store.entries)}")
    print("=" * 65)


if __name__ == "__main__":
    build_full_handbook_index(batch_size=25)