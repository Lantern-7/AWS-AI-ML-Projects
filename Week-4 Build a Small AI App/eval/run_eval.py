"""
Automated Evaluation Suite for AASTU RAG System.
Runs regression tests against a golden dataset to evaluate retrieval hit-rate,
factual grounding, schema validity, and hallucination resistance.
"""

import os
import sys
import json
import time
from typing import Dict, Any, List

# Add parent directory to path so we can import from src/
current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else "."
project_root = os.path.dirname(current_dir) if os.path.basename(current_dir) == "eval" else current_dir
sys.path.insert(0, project_root)

# Import RAG engine and vector store (works both locally and in Colab)
try:
    from src.rag_engine import RAGEngine, RAGResponse
    from src.vector_store import SimpleVectorStore
except ImportError:
    try:
        from rag_engine import RAGEngine, RAGResponse
        from vector_store import SimpleVectorStore
    except ImportError:
        # Fallback for interactive Colab memory
        if "RAGEngine" not in globals() or "SimpleVectorStore" not in globals():
            raise ImportError("Please run the vector_store and rag_engine cells first!")


def load_golden_dataset() -> List[Dict[str, Any]]:
    """Loads the test cases from disk."""
    candidates = [
        os.path.join("eval", "golden_dataset.json"),
        os.path.join(project_root, "eval", "golden_dataset.json"),
        "/content/eval/golden_dataset.json",
        "/content/golden_dataset.json",
        "golden_dataset.json",
    ]
    for p in candidates:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError("Could not find 'golden_dataset.json' in eval/ or current directory.")


def seed_test_knowledge_base(store: SimpleVectorStore) -> None:
    """Seeds the vector store with reference chunks to ensure repeatable evals."""
    reference_chunks = [
        {
            "chunk_id": "chunk_policy_1",
            "page_number": 42,
            "source": "AASTU Handbook",
            "text": "Academic Standing: A student must maintain a minimum Cumulative Grade Point Average (CGPA) of 2.00 to remain in good standing. Failure to do so leads to academic probation."
        },
        {
            "chunk_id": "chunk_policy_2",
            "page_number": 45,
            "source": "AASTU Handbook",
            "text": "Dismissal and Appeals: A student subject to academic dismissal may submit an appeal letter to the Academic Standards Committee within 10 working days of grade announcement."
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
    store.add_chunks(reference_chunks, batch_size=10)


def run_evaluation() -> None:
    print("=" * 65)
    print("      AASTU RAG PIPELINE - AUTOMATED EVALUATION SUITE")
    print("=" * 65)

    test_cases = load_golden_dataset()
    print(f"[OK] Loaded {len(test_cases)} golden test cases.\n")

    # 1. Initialize RAG system
    store = SimpleVectorStore()
    seed_test_knowledge_base(store)
    engine = RAGEngine(vector_store=store)

    results = []
    retrieval_hits = 0
    grounding_passes = 0
    schema_passes = 0

    print("Running test cases...\n")

    for idx, test in enumerate(test_cases, 1):
        t_id = test["test_id"]
        question = test["question"]
        expected_keywords = test["expected_keywords"]
        expected_page = test["expected_page"]
        should_ground = test["should_be_grounded"]

        print(f"[{idx}/{len(test_cases)}] Running: {t_id}")
        print(f"    Question: \"{question}\"")

        try:
            # Query the RAG engine
            response: RAGResponse = engine.query(question, top_k=2)
            schema_passes += 1

            # Check 1: Retrieval Hit Check
            retrieved_pages = [c.page_number for c in response.citations]
            hit = (expected_page in retrieved_pages) if expected_page else True
            if hit:
                retrieval_hits += 1

            # Check 2: Keyword / Grounding Check
            answer_lower = response.answer.lower()
            keywords_found = [kw for kw in expected_keywords if kw.lower() in answer_lower]
            keyword_pass = len(keywords_found) >= 1

            # Check 3: Hallucination check on out-of-scope question
            if not should_ground:
                # For out-of-scope, passing means it refused or flagged low confidence
                hallucination_safe = (
                    "cannot find" in answer_lower or 
                    "not" in answer_lower or 
                    not response.is_grounded or 
                    response.confidence_score < 0.6
                )
                test_passed = hallucination_safe
                status = "PASS (Safely Refused)" if test_passed else "FAIL (Hallucinated)"
            else:
                test_passed = hit and keyword_pass and response.is_grounded
                status = "PASS" if test_passed else "FAIL"

            if test_passed:
                grounding_passes += 1

            print(f"    Status: {status}")
            print(f"    Answer: \"{response.answer[:100]}...\"")
            print(f"    Citations: {retrieved_pages} | Expected Page: {expected_page}")
            print(f"    Keywords Found: {keywords_found}/{expected_keywords}\n")

            results.append({
                "test_id": t_id,
                "status": status,
                "passed": test_passed
            })

            time.sleep(1.0)  # Gentle spacing for API rate limits

        except Exception as e:
            print(f"    Status: ERROR ({e})\n")
            results.append({"test_id": t_id, "status": f"ERROR: {e}", "passed": False})

    # ==========================================
    # Final Scorecard Summary (Slide 10 & 14)
    # ==========================================
    total = len(test_cases)
    total_passed = sum(1 for r in results if r["passed"])
    accuracy = (total_passed / total) * 100
    hit_rate = (retrieval_hits / total) * 100

    print("=" * 65)
    print("                    EVALUATION SCORECARD")
    print("=" * 65)
    print(f"  Total Test Cases       : {total}")
    print(f"  Passed                 : {total_passed} / {total}")
    print(f"  Overall Accuracy       : {accuracy:.1f}%")
    print(f"  Schema Conformance     : {(schema_passes / total) * 100:.1f}%")
    print(f"  Retrieval Hit-Rate     : {hit_rate:.1f}%")
    print("=" * 65)

    if accuracy >= 75.0:
        print("[SUCCESS] Quality bar passed! Ready for production deployment.")
    else:
        print("[WARNING] Quality bar not met. Refine prompts or chunking.")
    print("=" * 65)


if __name__ == "__main__":
    run_evaluation()