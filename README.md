<div align="center">

# ☁️ AWS Student Builder Group — AI & ML Track
### Addis Ababa Science and Technology University (AASTU)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-FF6F61?style=for-the-badge)](https://www.trychroma.com/)
[![HuggingFace](https://img.shields.io/badge/Hugging%20Face-Embeddings-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)

<p align="center">
  A curated collection of practical AI, Machine Learning, and Cloud-native projects and laboratory submissions built during the <b>AWS Student Builder Group</b> program at <b>AASTU</b>.
</p>

[Weekly Projects](#-weekly-submissions) • [Repository Structure](#-repository-structure) • [Tech Stack](#-technologies--tools) • [Getting Started](#-getting-started)

</div>

---

## 📌 About the Track

The **AWS Student Builder Group (AI/ML Track)** is an intensive, hands-on program designed to build strong foundations in machine learning engineering, vector databases, data pipelines, and cloud-native AI deployment.

This repository tracks weekly milestone projects, transitioning from core data manipulation primitives to advanced retrieval systems (RAG) and cloud-ready architectures.

---

## 📂 Weekly Submissions

| Week | Project | Key Concepts | Tech Stack | Status | Quick Access |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **01** | **[Data Processing Pipeline](./Week-1-Data-Processing)** | Data sanitization, type coercion, missing value imputation, NumPy vectorization & boolean masking | `Python`, `NumPy` | Completed | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/19q0XB9RUrdkSReAn6FGaWbdIBFoQIQ2W) |
| **02** | **[Mini Semantic Search Engine](./Week-2%20Mini%20Semantic%20Search)** | Dense vector embeddings, ChromaDB, Cosine similarity, university FAQ semantic retrieval | `ChromaDB`, `Sentence-Transformers`, `Pandas` | Completed | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1RjCP4c_69brDS6ZIWp2UwKHAXX-7hrNg) |

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
│   └── week1_data_processing.py             # Reproducible standalone script
│
└── Week-2 Mini Semantic Search/             # Week 2: Vector search engine
    ├── README.md                            # Week 2 documentation
    ├── requirements.txt                     # Dependencies (chromadb, sentence-transformers, pandas)
    ├── week2_semantic_search.ipynb          # End-to-end orchestration notebook
    ├── week2_semantic_search.py             # Standalone pipeline script
    ├── Data/
    │   └── aastu_faqs.csv                   # Raw AASTU University FAQ dataset
    └── Src/
        ├── data_loader.py                   # Data ingestion, cleaning, and text chunking
        └── search_engine.py                 # ChromaDB wrapper for indexing and semantic query
```

---

## 🛠️ Technologies & Tools

- **Core Language:** Python 3.10+
- **Numerical & Data Processing:** NumPy, Pandas
- **Vector Storage & Retrieval:** ChromaDB
- **Embedding Models:** Sentence-Transformers (`all-MiniLM-L6-v2` via Hugging Face)
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
# Example for Week 2
cd "Week-2 Mini Semantic Search"
pip install -r requirements.txt
python week2_semantic_search.py
```

---

## 👨‍💻 Author

**Lantern-7**  
*AWS Student Builder Group — Addis Ababa Science and Technology University (AASTU)*  
GitHub: [@Lantern-7](https://github.com/Lantern-7)

---

<div align="center">
  <sub>Built with ❤️ for the AWS Student Builder Group AI/ML community at AASTU.</sub>
</div>
