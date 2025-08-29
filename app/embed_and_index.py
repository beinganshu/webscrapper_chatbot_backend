import faiss
import pickle
from sentence_transformers import SentenceTransformer
from utils import chunk_text

def build_faiss_index(pages_dict, model_name='all-MiniLM-L6-v2'):
    embedder = SentenceTransformer(model_name)
    chunks = []
    chunk_sources = []

    for url, content in pages_dict.items():
        for chunk in chunk_text(content):
            chunks.append(chunk)
            chunk_sources.append(url)

    embeddings = embedder.encode(chunks, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    with open("data/chunks.pkl", "wb") as f:
        pickle.dump({"chunks": chunks, "sources": chunk_sources}, f)
    faiss.write_index(index, "data/faiss_index.index")

    print(f"✅ Indexed {len(chunks)} chunks.")
