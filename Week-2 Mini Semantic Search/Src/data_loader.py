import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath)
        logging.info(f"Successfully loaded {len(df)} rows from {filepath}")
        df = df.dropna(subset=["question", "answer"])
        df["question"] = df["question"].str.strip()
        df["answer"] = df["answer"].str.strip()
        df["search_chunk"] = "Category: " + df["category"] + " | Q: " + df["question"] + " | A: " + df["answer"]
        return df
    except Exception as e:
        logging.error(f"Error: {e}")
        raise
