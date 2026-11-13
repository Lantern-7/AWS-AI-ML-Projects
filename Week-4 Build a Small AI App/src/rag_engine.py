"""
RAG Engine: Retrieve -> Augment -> Generate with Structured Pydantic Validation.
Loads system prompts from file, calls Gemini API, and validates outputs against
a strict Pydantic schema with automated repair retries.
"""

import os
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

# Import our previously built vector store
try:
    from src.vector_store import SimpleVectorStore, get_gemini_api_key
except ImportError:
    # Allows running directly when inside src/ or in Colab
    from vector_store import SimpleVectorStore, get_gemini_api_key


# ==========================================
# 1. Pydantic Models for Structured Output
# ==========================================
class Citation(BaseModel):
    chunk_id: str = Field(description="Unique ID of the source chunk")
    page_number: int = Field(description="Page number from the official handbook")
    source: str = Field(default="AASTU Handbook", description="Document source name")


class RAGResponse(BaseModel):
    answer: str = Field(description="Direct, factual answer to the question")
    citations: List[Citation] = Field(default_factory=list, description="List of source citations")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")
    is_grounded: bool = Field(description="True if the answer is directly supported by evidence")


# ==========================================
# 2. Complete RAG Engine Class
# ==========================================
class RAGEngine:
    def __init__(self, vector_store: SimpleVectorStore, prompt_path: Optional[str] = None):
        self.vector_store = vector_store
        self.api_key = vector_store.api_key
        self.prompt_template = self._load_prompt_template(prompt_path)

    def _load_prompt_template(self, prompt_path: Optional[str]) -> str:
        """Loads prompt from file as required by Slide 13."""
        candidates = [
            prompt_path,
            os.path.join("prompts", "system_prompt.txt"),
            os.path.join("..", "prompts", "system_prompt.txt"),
            "/content/prompts/system_prompt.txt",
            "/content/system_prompt.txt",
        ]
        for p in candidates:
            if p and os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()

        # Fallback default if file is missing
        return (
            "You are an academic advisor. Answer using ONLY the context.\n"
            "Output JSON: {\"answer\": string, \"citations\": [{\"chunk_id\": string, \"page_number\": int}], "
            "\"confidence_score\": float, \"is_grounded\": bool}\n\n"
            "CONTEXT:\n{context}\n\nQUESTION:\n{question}"
        )

    def _call_gemini(self, prompt: str) -> str:
        """Calls Gemini API requesting JSON structured output."""
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-flash-lite-latest:generateContent?key={self.api_key}"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.2  # Low temperature for factual, deterministic answers
            }
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        with urllib.request.urlopen(req) as resp:
            raw_response = json.loads(resp.read().decode("utf-8"))
            return raw_response["candidates"][0]["content"]["parts"][0]["text"].strip()

    def query(self, question: str, top_k: int = 3, max_repair_attempts: int = 2) -> RAGResponse:
        """
        Executes the full RAG pipeline:
        Retrieve -> Augment -> Generate -> Pydantic Validation & Repair Loop.
        """
        # Step 1: RETRIEVE
        retrieved_chunks = self.vector_store.search(question, top_k=top_k)

        # Step 2: AUGMENT
        context_parts = []
        for c in retrieved_chunks:
            context_parts.append(
                f"[Chunk: {c['chunk_id']} | Page: {c['page_number']}]\n{c['text']}"
            )
        context_str = "\n\n".join(context_parts)

        # Use .replace() so it doesn't conflict with JSON braces in the prompt
        full_prompt = (
            self.prompt_template
            .replace("{context}", context_str)
            .replace("{question}", question)
        )

        # Step 3 & 4: GENERATE with VALIDATION & REPAIR LOOP (Slide 6 & 13)
        current_prompt = full_prompt
        for attempt in range(max_repair_attempts + 1):
            raw_json = self._call_gemini(current_prompt)
            try:
                # Validate with Pydantic
                validated_response = RAGResponse.model_validate_json(raw_json)
                return validated_response
            except ValidationError as err:
                if attempt < max_repair_attempts:
                    print(f"[Repair Loop] Validation failed on attempt {attempt + 1}. Retrying with error...")
                    current_prompt = (
                        f"{full_prompt}\n\n"
                        f"CRITICAL ERROR: Your previous response violated the schema:\n{err}\n"
                        f"Please fix and output ONLY valid JSON."
                    )
                else:
                    raise RuntimeError(f"RAG output failed validation after {max_repair_attempts} retries: {err}")


if __name__ == "__main__":
    print("=== Testing Full RAG Engine ===")
    
    # 1. Initialize Vector Store
    store = SimpleVectorStore()
    
    # 2. Add sample chunks if empty
    if not store.entries:
        sample_chunks = [
            {
                "chunk_id": "chunk_policy_1",
                "page_number": 42,
                "source": "AASTU Handbook",
                "text": "Academic Standing: A student must maintain a minimum Cumulative Grade Point Average (CGPA) of 2.00 to remain in good standing. A student whose CGPA falls below 2.00 is placed on academic probation."
            },
            {
                "chunk_id": "chunk_policy_2",
                "page_number": 45,
                "source": "AASTU Handbook",
                "text": "Dismissal and Appeals: A student subject to academic dismissal may submit an appeal letter to the Academic Standards Committee within 10 working days of grade announcement."
            }
        ]
        store.add_chunks(sample_chunks)

    # 3. Create RAG Engine
    engine = RAGEngine(vector_store=store)

    # 4. Test question
    question = "What is the minimum CGPA for academic standing, and can I appeal if dismissed?"
    print(f"\nStudent Question: {question}\n")

    response = engine.query(question, top_k=2)

    print("--- Validated Structured RAG Response ---")
    print(f"Answer: {response.answer}\n")
    print(f"Confidence: {response.confidence_score * 100}% | Grounded: {response.is_grounded}")
    print("Citations:")
    for c in response.citations:
        print(f"  * Source: {c.source} | Page: {c.page_number} | Chunk: {c.chunk_id}")