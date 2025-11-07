from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from recommender.model import Recommender

app = FastAPI(title="SHL Assessment Recommender")
rec = Recommender()

class Req(BaseModel):
    query: str
    max_results: int = 10

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/recommend")
def recommend(req: Req):
    if not req.query or len(req.query.strip())<3:
        raise HTTPException(status_code=400, detail="Query too short")
    df = rec.recommend(req.query, k=min(max(1, req.max_results), 10))
    out = []
    for _, r in df.iterrows():
        out.append({
            "assessment_name": r['assessment_name'],
            "assessment_url": r['assessment_url'],
            "test_type": r.get('test_type','U'),
            "score": float(r.get('score',0.0))
        })
    return {"query": req.query, "recommendations": out}
