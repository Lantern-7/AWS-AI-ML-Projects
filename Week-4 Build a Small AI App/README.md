# 🎓 AASTU Academic AI Advisor (Production RAG Prototype)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render.com-brightgreen?style=for-the-badge&logo=render)](https://aastu-academic-advisor.onrender.com)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Gemini API](https://img.shields.io/badge/Google%20Gemini-Flash%20%26%20Embeddings-orange.svg)](https://aistudio.google.com/)
[![Pydantic v2](https://img.shields.io/badge/Validation-Pydantic%20v2-green.svg)](https://docs.pydantic.dev/)
[![Evaluation Pass](https://img.shields.io/badge/Golden%20Tests-100%25%20Passing-brightgreen.svg)]()

> 🌐 **Public Live Website:** [https://aastu-academic-advisor.onrender.com](https://aastu-academic-advisor.onrender.com)  
> *Available online for all Addis Ababa Science and Technology University (AASTU) students.*

An end-to-end, production-grade **Retrieval-Augmented Generation (RAG)** system built to answer questions regarding official university academic handbooks, grading policies, graduation criteria, and dismissal appeal processes. It features sliding-window chunking, vector semantic search, externalized prompts, strict **Pydantic schema validation**, and an automated regression test suite.

Developed as part of the **AWS AI & Machine Learning Mentorship Program (Week 4 & 5)**.

---

## 🏛️ System Architecture

```text
[ 1. USER INTERFACE ]
  Student Query: "What is the minimum CGPA?"
       │
       ▼  (app.py / Web UI / CLI)
[ 2. RETRIEVE ]
  ├── Convert question to 3072-dim vector via Gemini Embeddings
  ├── Calculate Cosine Similarity across cached handbook chunks
  └── Retrieve Top-3 most relevant handbook excerpts (Page 42, 45, etc.)
       │
       ▼
[ 3. AUGMENT ]
  ├── Load prompt template from prompts/system_prompt.txt
  └── Inject retrieved excerpts + strict Pydantic JSON schema
       │
       ▼
[ 4. GENERATE & VALIDATE ]
  ├── Gemini Flash generates structured JSON response
  ├── Pydantic validates: answer, citations, confidence_score, is_grounded
  └── Automated Repair Loop: retries with error logs if JSON is malformed
       │
       ▼
[ 5. VERIFIED RESPONSE ]
  Student receives: Answer + Grounded Badge + Page Citations
```

---

## 📂 Project Structure

```text
Week-4 Build a Small AI App/
├── App/
│   └── app.py                            # Production web server & interactive CLI
├── Data/
│   └── AASTU Student Academic Handbook.pdf # Official university knowledge base
├── eval/
│   ├── golden_dataset.json               # Curated regression test suite
│   └── run_eval.py                       # Automated evaluation runner & scorecard
├── prompts/
│   └── system_prompt.txt                 # Externalized prompt template & JSON schema
├── src/
│   ├── document_loader.py                # PDF parser & sliding-window chunker
│   ├── vector_store.py                   # Embedding generation, similarity & disk cache
│   └── rag_engine.py                     # Full RAG pipeline with Pydantic repair loop
├── web/
│   ├── index.html                        # AASTU-branded single-page application UI
│   └── logo.png                          # Official AASTU university crest & favicon
├── week4_Building_small_AI_app.ipynb     # Interactive Google Colab development notebook
├── week4_Building_small_AI_app.py        # Exported experimental development script
├── .env.example                          # Environment variable configuration template
├── .gitignore                            # Secret & vector cache protection
├── README.md                             # Comprehensive project documentation
└── requirements.txt                      # Project dependencies
```

---

## 🚀 Getting Started & Local Setup

### 1. Prerequisites
* Python 3.10+ (tested up to Python 3.14)
* A free Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### 2. Installation
```bash
git clone https://github.com/Lantern-7/AWS-AI-ML-Projects.git
cd "AWS-AI-ML-Projects/Week-4 Build a Small AI App"
pip install -r requirements.txt
```

### 3. Environment Variables
Create your local `.env` file from the provided template:
```bash
cp .env.example .env
```
Inside `.env`, insert your API key:
```ini
GEMINI_API_KEY=AIzaSyYourActualKeyHere
```

### 4. Running the Local Web App
```bash
python app.py
```
* Your default browser will automatically open to `http://localhost:8000`.

### 5. Running in Interactive CLI Mode
```bash
python app.py --cli
```

### 6. Interactive Google Colab Notebook
For step-by-step exploration, open `week4_Building_small_AI_app.ipynb` directly in Google Colab. It guides you through installing `pypdf`, uploading the handbook, inspecting vector distances, and testing individual RAG pipeline queries.

---

## 🎯 Prompt Engineering Choices

Following production AI best practices (Slide 5 & 13), prompt templates are **externalized in `prompts/system_prompt.txt`** rather than hardcoded in application logic.

### Design Principles:
1. **Persona Framing**: Guides the model as the *Official AASTU Academic Advisor*, enforcing an objective, helpful tone.
2. **Grounding & Abstention Constraint**: Explicitly restricts answers to provided handbook excerpts. If the information is not present, the model must abstain:
   > *"I cannot find this information in the official AASTU handbook."*
3. **Structured Output Contract**: Binds generation to a strict Pydantic JSON schema:
   ```json
   {
     "answer": "string",
     "citations": [{"chunk_id": "string", "page_number": 1}],
     "confidence_score": 0.95,
     "is_grounded": true
   }
   ```
4. **Delimited Context Blocks**: Separates system instructions from retrieved text using clear section boundaries (`--- CONTEXT EXCERPTS ---`) to guard against prompt injection.

### Example Outputs:

#### ✅ Example 1: In-Scope Query (Grounded with Citations)
* **Student Question**: *"What is the minimum CGPA for good academic standing, and can I appeal if dismissed?"*
* **RAG Response**:
  ```json
  {
    "answer": "To remain in good academic standing, a student must maintain a minimum Cumulative Grade Point Average (CGPA) of 2.00. If subject to academic dismissal, a student may submit an appeal letter to the Academic Standards Committee within 10 working days of grade announcement.",
    "citations": [
      {
        "chunk_id": "chunk_policy_1",
        "page_number": 42,
        "source": "AASTU Handbook"
      },
      {
        "chunk_id": "chunk_policy_2",
        "page_number": 45,
        "source": "AASTU Handbook"
      }
    ],
    "confidence_score": 1.0,
    "is_grounded": true
  }
  ```

#### 🛡️ Example 2: Out-of-Scope / Adversarial Query (Hallucination Defense)
* **Student Question**: *"What is the secret recipe for the campus cafeteria's special burger sauce?"*
* **RAG Response**:
  ```json
  {
    "answer": "I cannot find this information in the official AASTU handbook.",
    "citations": [],
    "confidence_score": 0.0,
    "is_grounded": false
  }
  ```

---

## 📊 Automated Evaluation Suite & Scorecard

Per **Slide 10 & 14**, evaluation is essential for tracking regression and ensuring reliability. We implemented an automated evaluation runner (`eval/run_eval.py`) that evaluates our RAG engine against `eval/golden_dataset.json`.

### Run Automated Evals:
```bash
python eval/run_eval.py
```

### Final Scorecard Results:

| Benchmark Metric | Target Threshold | Measured Score | Status |
| :--- | :---: | :---: | :---: |
| **Total Test Cases** | 4 | 4 | Complete |
| **Passed Tests** | $\ge 75\%$ | **4 / 4 (100.0%)** | **PASSED** |
| **Overall Accuracy** | $\ge 75\%$ | **100.0%** | **PASSED** |
| **Pydantic Schema Conformance** | $100\%$ | **100.0%** | **PASSED** |
| **Retrieval Hit-Rate** | $\ge 80\%$ | **100.0%** | **PASSED** |
| **Hallucination Resistance** | $100\%$ | **100.0%** | **PASSED** |

---

## 🛡️ Responsible AI, Safety, & Privacy

* **Hallucination Prevention**: Non-parametric retrieval grounds all factual claims. The model abstains rather than inventing policies.
* **Prompt Injection Mitigation**: Retrieved handbook text is delimited and treated purely as passive data, preventing instruction overrides.
* **Privacy & Least Privilege**: No student identity or credentials are stored or transmitted. The API key is loaded strictly through environment variables.
* **Source Transparency**: Every answer includes page numbers and chunk identifiers, allowing students to verify claims in their physical handbooks.

---

## 🔮 Future Roadmap (Week 5 Production RAG)
* [ ] **Hybrid Search**: Combine dense vector retrieval with BM25 keyword matching for exact numerical policy lookups.
* [ ] **Cross-Encoder Reranking**: Implement a second-stage reranker to score candidate passages before prompt injection.
* [ ] **AWS Cloud Deployment**: Migrate backend to AWS App Runner / Amazon Bedrock.

---

## 👨‍💻 Author
**Ermiyas Getachew**  
Addis Ababa Science and Technology University (AASTU)