import faiss, pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = "all-mpnet-base-v2"

class Recommender:
    def __init__(self, index_path="data/shl_index.faiss", catalog_parquet="data/shl_catalog.parquet"):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(index_path)
        self.df = pd.read_parquet(catalog_parquet)

    def classify_query(self, q):
        ql = q.lower()
        tech = any(tok in ql for tok in ["java","python","sql","javascript","react","node","c++","c#"])
        beh = any(tok in ql for tok in ["team","collaborate","communication","stakeholder","behaviour","behavior","personality"])
        return tech, beh

    def recommend(self, query, k=10):
        emb = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(emb)
        D, I = self.index.search(emb, 50)
        cand = self.df.iloc[I[0]].copy()
        cand['score'] = D[0]
        tech, beh = self.classify_query(query)
        if tech and beh:
            tech_cand = cand[cand.test_type=="K"].nlargest(int(k*0.4), 'score')
            beh_cand = cand[cand.test_type=="P"].nlargest(int(k*0.4), 'score')
            selection = pd.concat([tech_cand, beh_cand])
            remaining = k - len(selection)
            others = cand[~cand.index.isin(selection.index)].nlargest(remaining, 'score')
            res = pd.concat([selection, others]).head(k)
        else:
            res = cand.nlargest(k, 'score')
        return res[['assessment_name','assessment_url','test_type','score']]
