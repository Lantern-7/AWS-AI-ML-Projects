"""
Document Loader and Chunker for the AASTU Academic Handbook.
Reads PDF files and splits them into clean, overlapping text chunks with metadata.
"""

import os
from typing import List, Dict, Any
from pypdf import PdfReader


def find_handbook_path() -> str:
    """
    Locates the handbook PDF reliably across any working directory.
    Uses __file__ to anchor paths directly to the project folder.
    """
    # 1. Anchor to project root (one level up from src/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    candidates = [
        os.path.join(project_root, "Data", "AASTU Student Academic Handbook.pdf"),
        os.path.join(script_dir, "..", "Data", "AASTU Student Academic Handbook.pdf"),
        os.path.join("Data", "AASTU Student Academic Handbook.pdf"),
        os.path.join(script_dir, "Data", "AASTU Student Academic Handbook.pdf"),
        "/content/AASTU Student Academic Handbook.pdf",
        "AASTU Student Academic Handbook.pdf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return os.path.abspath(path)

    raise FileNotFoundError(
        f"Could not find 'AASTU Student Academic Handbook.pdf'. Checked locations:\n"
        + "\n".join(f" - {p}" for p in candidates)
    )


def load_pdf_pages(pdf_path: str = None) -> List[Dict[str, Any]]:
    """
    Reads a PDF file and extracts text page by page.
    
    Args:
        pdf_path: Path to PDF. If None, auto-locates using find_handbook_path().
    """
    if pdf_path is None:
        pdf_path = find_handbook_path()

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    reader = PdfReader(pdf_path)
    pages_data = []

    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        # Clean up excessive whitespace
        cleaned_text = " ".join(text.split())
        if cleaned_text:
            pages_data.append({
                "page_number": idx + 1,
                "text": cleaned_text
            })

    return pages_data


def chunk_text(
    pages_data: List[Dict[str, Any]], 
    chunk_size: int = 1000, 
    chunk_overlap: int = 200
) -> List[Dict[str, Any]]:
    """
    Splits page text into smaller overlapping chunks with metadata.
    
    Args:
        pages_data: List of page dicts from load_pdf_pages.
        chunk_size: Maximum characters per chunk (approx. 100-150 words).
        chunk_overlap: Number of characters shared between consecutive chunks.
    """
    chunks = []
    chunk_counter = 0

    for page in pages_data:
        text = page["text"]
        page_num = page["page_number"]
        start = 0

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

            start += (chunk_size - chunk_overlap)

    return chunks


if __name__ == "__main__":
    pdf_path = find_handbook_path()
    print(f"Located PDF at: {pdf_path}")
    pages = load_pdf_pages(pdf_path)
    print(f"[OK] Successfully loaded {len(pages)} pages.")
    all_chunks = chunk_text(pages)
    print(f"[OK] Generated {len(all_chunks)} searchable chunks.")