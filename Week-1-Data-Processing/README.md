# Week 1: Small Python Data-Processing App & Weather Analyst

This folder contains two projects for Week 1:
1. **Data Processing App:** A script that loads a raw list, cleans it using functions, and processes it with NumPy.
2. **Weather Analyst:** A practical project that fetches API data, cleans it with Pandas, trains a Random Forest ML model, and uses a Gemini AI Agent.

## ⚙️ Environment Setup (venv)
This project uses a virtual environment to manage dependencies. The `.venv/` folder is ignored via `.gitignore`.

To recreate the environment:
1. Create a virtual environment:
   `python -m venv .venv`
2. Activate it:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`

## 🚀 How to Run
**Option A: Google Colab (Recommended)**
Open the `.ipynb` files directly in Google Colab. All outputs are saved in the notebook.

**Option B: Local Python**
Run the `.py` scripts in your terminal:
`python data_processing_app.py`
`python weather_analyst.py`