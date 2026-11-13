<div align="center">

# ☁️ AWS Student Builder Group — AI & ML Track
### Addis Ababa Science and Technology University (AASTU)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Flash%20%26%20Embeddings-FFA116?style=for-the-badge&logo=googlegemini&logoColor=white)](https://aistudio.google.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-FF6F61?style=for-the-badge)](https://www.trychroma.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Live Demo](https://img.shields.io/badge/Render-Live%20Demo-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://aastu-academic-advisor.onrender.com)

<p align="center">
  A curated collection of practical AI, Machine Learning, and Cloud-native projects and laboratory submissions built during the <b>AWS Student Builder Group</b> program at <b>AASTU</b>.
</p>

[Weekly Projects](#-weekly-submissions) • [Repository Structure](#-repository-structure) • [Tech Stack](#-technologies--tools) • [Getting Started](#-getting-started)

</div>

---

## 📌 About the Track

The **AWS Student Builder Group (AI/ML Track)** is an intensive, hands-on program designed to build strong foundations in machine learning engineering, vector databases, data pipelines, and cloud-native AI deployment.

This repository tracks weekly milestone projects, transitioning from core data manipulation primitives and classical statistical NLP to modern dense retrieval systems, production-grade **Retrieval-Augmented Generation (RAG)**, automated evaluation harnesses, and full-stack generative AI applications.

---

## 📂 Weekly Submissions

| Week | Project | Key Concepts | Tech Stack | Status | Quick Access |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **01** | **[Data Processing Pipeline](./Week-1-Data-Processing)** | Data sanitization, type coercion, missing value imputation, NumPy vectorization & boolean masking | `Python`, `NumPy` | Completed | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/19q0XB9RUrdkSReAn6FGaWbdIBFoQIQ2W) |
| **02** | **[Mini Semantic Search Engine](./Week-2%20Mini%20Semantic%20Search)** | Dense vector embeddings, ChromaDB, Cosine similarity, university FAQ semantic retrieval | `ChromaDB`, `Sentence-Transformers`, `Pandas` | Completed | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1RjCP4c_69brDS6ZIWp2UwKHAXX-7hrNg) |
| **03** | **[Spam Detection & Classical ML](./Week-3%20Spam%20filter)** | TF-IDF tokenization, Multinomial Naive Bayes, adversarial evasion analysis, Bag-of-Words vs. LLMs | `scikit-learn`, `Pandas` | Completed | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Bm4YgGYSUNGivXSCsnoBLKibcOw5hNht) |
| **04** | **[AASTU Academic AI Advisor (RAG)](./Week-4%20Build%20a%20Small%20AI%20App)** | Production RAG pipeline, PDF parsing (`pypdf`), Gemini 3072-dim embeddings, vector disk caching, externalized prompts, strict Pydantic schema validation with repair retry loop, automated golden evaluation suite (100% pass), web & CLI interfaces | `Gemini API`, `Pydantic v2`, `pypdf`, `HTML5/CSS3` | Completed / Live | [![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen.svg)](https://aastu-academic-advisor.onrender.com) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1WwSCrRu6sU4xD3BeGuRKXW2xf7MvaurD) |

---

## 🏗️ Repository Structure

```plaintext
AWS-AI-ML-Projects/
│
├── README.md                                # Root repository guide
│
├── Week-1-Data-Processing/                  # Week 1: Data pipeline & NumPy
│   ├── README.md                            # Week 1 documentation
│   ├── requirements.txt                     # Dependencies (numpy)
│   ├── week1_data_processing.ipynb          # Interactive Colab notebook
│   └── week1_data_processing.py             # Standalone Python script
│
├── Week-2 Mini Semantic Search/             # Week 2: Vector search engine
│   ├── README.md                            # Week 2 documentation
│   ├── requirements.txt                     # Dependencies (chromadb, sentence-transformers, pandas)
│   ├── week2_semantic_search.ipynb          # End-to-end orchestration notebook
│   ├── week2_semantic_search.py             # Standalone pipeline script
│   ├── Data/
│   │   └── aastu_faqs.csv                   # Raw AASTU University FAQ dataset
│   └── Src/
│       ├── data_loader.py                   # Data ingestion, cleaning, and text chunking
│       └── search_engine.py                 # ChromaDB wrapper for indexing and semantic query
│
├── Week-3 Spam filter/                      # Week 3: Classical ML & Adversarial Testing
│   ├── README.md                            # Week 3 documentation & vulnerability analysis
│   ├── requirements.txt                     # Dependencies (pandas, scikit-learn)
│   ├── week3_spam_filter.ipynb              # Interactive Colab notebook with benchmarks
│   └── week3_spam_filter.py                 # Standalone classification script
│
└── Week-4 Build a Small AI App/             # Week 4 & 5: Production RAG Prototype & Academic Advisor
    ├── README.md                            # Comprehensive RAG documentation, architecture & scorecards
    ├── requirements.txt                     # Dependencies (pydantic, pypdf, python-dotenv)
    ├── app.py                               # Production web server (localhost:8000) & CLI runner
    ├── week4_Building_small_AI_app.ipynb    # Interactive Google Colab notebook
    ├── week4_building_small_ai_app.py       # Standalone pipeline development script
    ├── .env.example                         # Environment variable configuration template
    ├── Data/
    │   └── AASTU Student Academic Handbook.pdf # Official university knowledge base
    ├── eval/
    │   ├── golden_dataset.json              # Curated regression test suite
    │   └── run_eval.py                      # Automated evaluation runner & scorecard
    ├── prompts/
    │   └── system_prompt.txt                # Externalized prompt template & JSON schema
    ├── src/
    │   ├── document_loader.py               # PDF parser & sliding-window chunker
    │   ├── vector_store.py                  # Gemini embeddings, cosine similarity & disk cache
    │   └── rag_engine.py                    # Full RAG pipeline with Pydantic repair loop
    └── web/
        ├── index.html                       # AASTU-branded single-page application UI
        └── logo.png                         # University crest & favicon branding asset
```

---

## 🛠️ Technologies & Tools

- **Core Language:** Python 3.10+ (tested up to Python 3.14)
- **Generative AI & LLMs:** Google Gemini (`gemini-1.5-flash` / Gemini Flash & Gemini Embeddings)
- **Data Validation & Guardrails:** Pydantic v2 (Strict type enforcement, automated repair retry loops)
- **Document Ingestion & Chunking:** `pypdf` (sliding-window chunking with page-level metadata)
- **Vector Storage & Retrieval:** ChromaDB, custom in-memory vector store with cosine similarity & disk caching
- **Machine Learning & Classical NLP:** scikit-learn (`TfidfVectorizer`, `MultinomialNB`, metrics)
- **Numerical & Data Processing:** NumPy, Pandas
- **Web Interface & Deployment:** Native Python HTTP server, HTML5/CSS3/Vanilla JS UI, hosted on Render.com
- **Environments:** Google Colab, Python `venv`

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Lantern-7/AWS-AI-ML-Projects.git
cd AWS-AI-ML-Projects
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Running an Individual Week
Each week is self-contained with its own dependencies and execution scripts. Navigate to the desired folder:

```bash
# Example: Week 4 (AASTU Academic AI Advisor RAG)
cd "Week-4 Build a Small AI App"
pip install -r requirements.txt
cp .env.example .env    # Configure GEMINI_API_KEY inside .env

# Launch the Web App (opens in browser at http://localhost:8000)
python app.py

# Or run the automated evaluation suite
python eval/run_eval.py
```

---

## 👨‍💻 Author

**Ermiyas Getachew**  
*AWS Student Builder Group — Addis Ababa Science and Technology University (AASTU)*  
GitHub: [@Lantern-7](https://github.com/Lantern-7)

---

<div align="center">
  <sub>Built with ❤️ for the AWS Student Builder Group AI/ML community at AASTU.</sub>
</div>
