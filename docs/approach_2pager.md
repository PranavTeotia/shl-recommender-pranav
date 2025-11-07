SHL Assessment Recommendation — Approach & Optimization (2 pages)

Problem summary
Hiring teams need relevant SHL assessments given a natural-language job description (JD). We built a retrieval-first recommendation system that returns 5–10 individual test solutions from SHL’s product catalog, balancing technical (K) and behavioral/personality (P) assessments when the JD spans domains.

Data pipeline
1. Catalog crawling — A small crawler extracts individual product pages from SHL’s product catalog URL and stores assessment_name, assessment_url, test_type, short_description, and full_text. We explicitly filter out “Pre-packaged Job Solutions”.
2. Text normalization — Concatenate name + description + metadata; lowercase, remove boilerplate, and preserve key metadata tags like test_type.
3. Representation — Generate dense embeddings with sentence-transformers (all-mpnet-base-v2) for reproducibility and cost-efficiency. Embeddings normalized and stored in a FAISS Index.
4. Storage — Parquet for metadata, FAISS file for vectors. Both persisted to S3 or blob storage for production.

Retrieval & ranking strategy
1. Semantic retrieval — Encode the JD, retrieve top-N (50) candidates by cosine similarity (FAISS).
2. Query intent classification — Lightweight rules + keywords to detect technical vs behavioral intent (e.g., presence of “Java”, “SQL” → technical; “collaborate”, “team” → behavioral). This feeds balancing logic.
3. Reranking — Re-rank top candidates by combining cosine score with simple boosts: exact keyword matches, test_type matching, and optional LLM-based reranker for top 20 results when compute budget allows.
4. Balance enforcement — If both technical and behavioral signals exist, enforce at least 30–50% coverage from each domain (configurable).

API & frontend
- GET /health — health check.
- POST /recommend — accepts {"query": "...", "max_results": 10} and returns JSON list of recommendations with assessment_name, assessment_url, test_type, score.
- Small React demo lets hiring managers paste JD text and preview top-10; supports CSV export.
