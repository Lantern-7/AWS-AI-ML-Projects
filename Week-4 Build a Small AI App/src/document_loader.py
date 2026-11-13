"""
Document Loader and Chunker for the AASTU Academic Handbook.
Reads PDF files and splits them into clean, overlapping text chunks with metadata.
"""

import os
from typing import List, Dict, Any
from pypdf import PdfReader


def load_pdf_pages(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Reads a PDF file and extracts text page by page.
    
    Args:
        pdf_path: Absolute or relative path to the PDF file.
        
    Returns:
        A list of dictionaries, where each item contains:
        - page_number: The 1-based page index.
        - text: The raw text extracted from that page.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    reader = PdfReader(pdf_path)
    pages_data = []

    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        # Clean up excessive whitespace and line breaks
        cleaned_text = " ".join(text.split())
        if cleaned_text:
            pages_data.append({
                "page_number": idx + 1,
                "text": cleaned_text
            })

    return pages_data


def chunk_text(
    pages_data: List[Dict[str, Any]], 
    chunk_size: int = 600, 
    chunk_overlap: int = 100
) -> List[Dict[str, Any]]:
    """
    Splits page text into smaller overlapping chunks with metadata.
    
    Args:
        pages_data: List of page dicts from load_pdf_pages.
        chunk_size: Maximum characters per chunk (approx. 100-150 words).
        chunk_overlap: Number of characters shared between consecutive chunks.
        
    Returns:
        List of chunks with metadata: text, page_number, chunk_id, and source.
    """
    chunks = []
    chunk_counter = 0

    for page in pages_data:
        text = page["text"]
        page_num = page["page_number"]
        start = 0

        # Slide a window across the page text
        while start < len(text):
            end = start + chunk_size
            chunk_slice = text[start:end].strip()

            if chunk_slice:
                chunk_counter += 1
                chunks.append({
                    "chunk_id": f"chunk_{chunk_counter}",
                    "page_number": page_num,
                    "source": "AASTU Student Academic Handbook",
                    "text": chunk_slice
                })

            # Move forward by (chunk_size - chunk_overlap)
            start += (chunk_size - chunk_overlap)

    return chunks


def find_handbook_path() -> str:
    """Helper to locate the handbook PDF both locally and in Google Colab."""
    candidates = [
        os.path.join("Data", "AASTU Student Academic Handbook.pdf"),
        os.path.join("..", "Data", "AASTU Student Academic Handbook.pdf"),
        "/content/AASTU Student Academic Handbook.pdf",
        "AASTU Student Academic Handbook.pdf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        "Could not find 'AASTU Student Academic Handbook.pdf' in Data/ or current directory."
    )


if __name__ == "__main__":
    # Self-test block: runs when executed directly
    pdf_path = find_handbook_path()
    print(f"Testing document loader with: {pdf_path}")
    
    pages = load_pdf_pages(pdf_path)
    print(f"[OK] Successfully loaded {len(pages)} pages.")
    
    all_chunks = chunk_text(pages, chunk_size=600, chunk_overlap=100)
    print(f"[OK] Generated {len(all_chunks)} searchable chunks.")
    
    if all_chunks:
        first = all_chunks[0]
        print("\n--- Example First Chunk ---")
        print(f"ID: {first['chunk_id']} | Page: {first['page_number']}")
        print(f"Text preview: {first['text'][:200]}...")