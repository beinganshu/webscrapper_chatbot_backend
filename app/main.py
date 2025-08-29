# backend/main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from web_scraper import scrape_site
from embed_and_index import build_faiss_index
from query_pipeline import RAGPipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str

@app.post("/scrape")
def scrape_endpoint(data: ScrapeRequest):
    pages = scrape_site(data.url, max_pages=5)
    build_faiss_index(pages)
    return {"status": "Scraping and indexing complete."}

@app.post("/ask")
def ask_question(data: QuestionRequest):
    rag = RAGPipeline()
    answer = rag.query(data.question)
    return {"answer": answer}