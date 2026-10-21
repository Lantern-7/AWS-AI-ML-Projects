# Week 1: Small Python Data-Processing App

## 📝 Project Overview
This assignment is a Python data-processing script that demonstrates the foundational data pipeline: Loading raw data, cleaning it with custom functions, and processing the results using NumPy. 

The project is built to run inside a Jupyter/Colab notebook, with a local Python script (`.py`) provided for reproducibility.

## ⚙️ Environment Setup (Virtual Environment)
This project requires a Python virtual environment (`.venv`) to manage dependencies. The `.venv` folder is intentionally excluded from this repository to keep it clean.

To recreate the environment and run the code locally:
1. Create the virtual environment:
   `python -m venv .venv`
2. Activate the environment:
   - **Windows PowerShell:** `.venv\Scripts\Activate.ps1`
   - **Mac/Linux:** `source .venv/bin/activate`
3. Install the required packages:
   `pip install -r requirements.txt`

## 🚀 How to Run
You can run this project in two ways:

**Option 1: Google Colab (Recommended)**
Open the `data_processing.ipynb` file in this folder using Google Colab. The notebook contains the full code, outputs, and explanations.

**Option 2: Local Python Script**
Run the standalone Python script in your terminal:
`python data_processing_app.py`

## 🧠 What the Code Does
1. **Loads Raw Data:** Initializes a messy dataset (a list of lists) containing missing values and text mixed with numbers.
2. **Cleans Data (Functions):** Uses `clean_number()` and `clean_dataset()` functions to safely convert strings to floats and handle missing values (`"unknown"` → `0.0`).
3. **Processes with NumPy:** Converts the clean data into a NumPy array to calculate the average age and salary, and filters for employees earning over $52,000 using vectorized boolean masking.