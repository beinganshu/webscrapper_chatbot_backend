import faiss
import pickle
from sentence_transformers import SentenceTransformer
from groq import Groq

GROQ_API_KEY = "YOUR_API_KEY"

class RAGPipeline:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.read_index("data/faiss_index.index")
        with open("data/chunks.pkl", "rb") as f:
            data = pickle.load(f)
        self.chunks = data["chunks"]
        self.sources = data["sources"]
        self.groq = Groq(api_key=GROQ_API_KEY)

    def query(self, question, top_k=5):
        q_embedding = self.embedder.encode([question])
        D, I = self.index.search(q_embedding, top_k)
        retrieved_chunks = [self.chunks[i] for i in I[0]]
        context = "\n\n".join(retrieved_chunks)

        prompt = f"""Answer the question using the context below. Be concise.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"""

        response = self.groq.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()

