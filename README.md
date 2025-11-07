# SHL Recommender (sample)
This archive contains the crawler, indexer, recommender, API and frontend demo files described in the chat. 
Use the scripts to crawl SHL product pages (if allowed), build an embedding index, run the FastAPI recommender, and run the React demo.

🧠 GenAI Assessment Recommendation — SHL Product Catalog RAG Tool

Author: Pranav Teotia
Role: AI Intern – Generative AI Assignment

📘 Overview

This project implements a Retrieval-Augmented Generation (RAG) system that recommends the most relevant SHL Assessments based on any given job description or hiring query.

The tool allows hiring teams to instantly identify individual SHL test solutions (e.g., cognitive, technical, behavioral) that match the job’s skill requirements.
It includes a FastAPI backend, React frontend, and an embedding-based recommendation engine built with sentence-transformers and FAISS.

🎯 Objective

“Given a natural-language job description, recommend the top 5–10 relevant SHL assessments.”

Key features

Crawls SHL’s product catalog and builds an internal dataset of assessments.

Uses semantic embeddings to map text similarity between a JD and assessment descriptions.

Balances technical (K) and personality/behavioral (P) assessments when needed.

Exposes a REST API and a web-based UI for exploration and testing.

⚙️ Architecture
+---------------------+
|   SHL Product Data  |
| (name, URL, desc.)  |
+---------+-----------+
          |
          v
  [Crawl & Clean Text]
          |
          v
 [Sentence Embeddings]
          |
          v
     [FAISS Index]
          |
          v
  +-------------------+
  | FastAPI Backend   |
  |  /recommend API   |
  +-------------------+
          |
          v
  +-------------------+
  | React Frontend    |
  |  (Vercel Deploy)  |
  +-------------------+

🧩 Tech Stack
Layer	Tools / Libraries
Backend	Python, FastAPI, FAISS, Sentence-Transformers
Frontend	React.js (Vercel)
Data	BeautifulSoup (Web Scraping), Pandas
Model	all-mpnet-base-v2 (text embeddings)
Infra	Docker, Render (backend), GitHub Actions (CI/CD)
