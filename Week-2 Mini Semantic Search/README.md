# Week 2: Mini Semantic Search Engine

A professional implementation of a semantic search engine over a University FAQ dataset. It uses embeddings to find answers based on *meaning* rather than exact keyword matching.

## 🏗️ Architecture
This project separates data, logic, and execution:
- `data/aastu_faqs.csv`: The raw CSV dataset.
- `src/data_loader.py`: Loads, cleans, and formats the text chunks.
- `src/search_engine.py`: Encapsulates ChromaDB for vector storage and cosine similarity search.
- `week2_semantic_search.ipynb`: The main notebook that orchestrates the pipeline.

## 🚀 How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Open `week2_semantic_search.ipynb` in Google Colab.
3. Run the cells sequentially.

## 💡 Example Query
The system is robust against vocabulary mismatch:
- **Query:** *"I can't log into the student portal to pick my courses."*
- **Top Match (Distance: 0.8372):** *"Registration | Q: How do I register for my classes? | A: Log into portal.aastu.edu.et using your student ID..."*

## 🛠️ Tech Stack
Python, Pandas, ChromaDB, Sentence-Transformers (Hugging Face).