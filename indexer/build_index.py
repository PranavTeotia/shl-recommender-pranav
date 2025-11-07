import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

MODEL_NAME = "all-mpnet-base-v2"

def build(shl_csv="data/shl_catalog.csv", index_out="data/shl_index.faiss", parquet_out="data/shl_catalog.parquet"):
    df = pd.read_csv(shl_csv)
    model = SentenceTransformer(MODEL_NAME)
    texts = df['full_text'].fillna("").tolist()
    embs = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    faiss.normalize_L2(embs)
    d = embs.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embs)
    faiss.write_index(index, index_out)
    df.to_parquet(parquet_out, index=False)
    print("Saved index and parquet.")

if __name__ == "__main__":
    build()
