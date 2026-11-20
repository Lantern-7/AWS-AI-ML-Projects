"""
AASTU Academic AI Advisor - Application Server & CLI.
Provides both a browser-based single-page web UI (with AASTU branding & logo)
and an interactive terminal mode.
"""

import os
import sys
import json
import argparse
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import List, Dict, Any

# Define base paths cleanly at module level
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

# Add both to sys.path so src/ is always discoverable
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from src.vector_store import SimpleVectorStore
from src.rag_engine import RAGEngine, RAGResponse


def seed_knowledge_base(store: SimpleVectorStore) -> None:
    """Loads cached embeddings or seeds core handbook chapters."""
    cache_candidates = [
        os.path.join(CURRENT_DIR, "src", "vector_cache", "handbook_embeddings.json"),
        os.path.join(PARENT_DIR, "src", "vector_cache", "handbook_embeddings.json"),
        os.path.join(CURRENT_DIR, "vector_cache", "handbook_embeddings.json"),
    ]
    cache_path = next((p for p in cache_candidates if os.path.exists(p)), cache_candidates[0])

    if store.load_cache(cache_path):
        return

    print("No existing vector cache found. Seeding initial handbook knowledge...")
    sample_handbook_chunks = [
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
    store.add_chunks(sample_handbook_chunks)
    store.save_cache(cache_path)


# ==========================================
# 1. Web Server Handler
# ==========================================
class RAGHTTPRequestHandler(SimpleHTTPRequestHandler):
    engine: RAGEngine = None

    def _get_web_dir(self) -> str:
        candidates = [
            os.path.join(CURRENT_DIR, "web"),
            os.path.join(PARENT_DIR, "web"),
            os.path.join(CURRENT_DIR, "..", "web"),
        ]
        return next((d for d in candidates if os.path.exists(d)), CURRENT_DIR)

    def do_GET(self):
        """Serves index.html, logo.png, and favicon."""
        web_dir = self._get_web_dir()

        # Serve index.html
        if self.path in ["/", "/index.html"]:
            html_path = os.path.join(web_dir, "index.html")
            if os.path.exists(html_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(html_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Serve logo / favicon
        if self.path in ["/logo.png", "/favicon.ico"]:
            logo_path = os.path.join(web_dir, "logo.png")
            if os.path.exists(logo_path):
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.end_headers()
                with open(logo_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        super().do_GET()

    def do_POST(self):
        """API Endpoint: /api/query."""
        if self.path == "/api/query":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_body.decode("utf-8"))
                question = data.get("question", "").strip()

                if not question:
                    self._send_json({"error": "Empty question provided"}, status=400)
                    return

                # Execute RAG query
                response: RAGResponse = self.engine.query(question, top_k=5)
                self._send_json(response.model_dump())

            except Exception as e:
                self._send_json({"error": str(e)}, status=500)
        else:
            self.send_error(404, "Endpoint Not Found")

    def _send_json(self, payload: Dict[str, Any], status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))


def run_web(engine: RAGEngine, port: int = None) -> None:
    """Launches the HTTP web server and binds to public host for deployment."""
    # Read PORT from cloud environment (Render/AWS) or default to 8000
    server_port = port or int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"  # Allows incoming traffic from the internet

    RAGHTTPRequestHandler.engine = engine
    server_address = (host, server_port)
    httpd = HTTPServer(server_address, RAGHTTPRequestHandler)

    url = f"http://localhost:{server_port}"
    print("=" * 65)
    print(f"  AASTU ACADEMIC AI ADVISOR - SERVER ONLINE")
    print(f"  Listening on: {host}:{server_port}")
    print("=" * 65)

    # Only open browser if running locally on desktop
    if "PORT" not in os.environ:
        webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("Server stopped cleanly.")


# ==========================================
# 2. Terminal Interactive CLI Mode
# ==========================================
def run_cli(engine: RAGEngine) -> None:
    """Runs interactive terminal chat mode."""
    print("=" * 65)
    print("  AASTU ACADEMIC AI ADVISOR - INTERACTIVE TERMINAL CHAT")
    print("  Type your question and press Enter. Type 'exit' to quit.")
    print("=" * 65)

    while True:
        try:
            question = input("\nStudent > ").strip()
            if not question:
                continue
            if question.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            print("Thinking and verifying sources...")
            response: RAGResponse = engine.query(question, top_k=3)

            print(f"\nAI Advisor: {response.answer}")
            print(f"Confidence: {response.confidence_score * 100:.0f}% | Grounded: {response.is_grounded}")
            if response.citations:
                print("Citations:")
                for c in response.citations:
                    print(f"  - {c.source} (Page {c.page_number}) [{c.chunk_id}]")

        except KeyboardInterrupt:
            print("\nExiting chat...")
            break


# ==========================================
# Main Entry Point
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AASTU Student Academic Advisor RAG App")
    parser.add_argument("--cli", action="store_true", help="Run in terminal CLI mode instead of launching web UI")
    parser.add_argument("--port", type=int, default=8000, help="Web server port (default: 8000)")
    args = parser.parse_args()

    store = SimpleVectorStore()
    seed_knowledge_base(store)
    engine = RAGEngine(vector_store=store)

    if args.cli:
        run_cli(engine)
    else:
        run_web(engine, port=args.port)