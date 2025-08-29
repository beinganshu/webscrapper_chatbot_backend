# test_pipeline.py

from web_scraper import scrape_site
from embed_and_index import build_faiss_index
from query_pipeline import RAGPipeline
import os

# Step 1: Scrape the site
print("🔍 Scraping website...")
url = "https://krack.ai/"  # Replace with the actual site
pages = scrape_site(url, max_pages=5)

# Step 2: Build vector DB
print("🧠 Building FAISS index...")
os.makedirs("data", exist_ok=True)
build_faiss_index(pages)

# Step 3: Load RAG pipeline
print("💬 Initializing RAG pipeline...")
rag = RAGPipeline()

# Step 4: Ask a question
question = "Can I learn guitar related courses from this website?"
print(f"❓ Question: {question}")
answer = rag.query(question)
print(f"✅ Answer: {answer}")