from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient("http://localhost:6333")
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_knowledge_base(question: str, threshold: float = 0.78) -> dict | None:
    embedding = model.encode(question).tolist()
    hits = client.search(collection_name="math_kb", query_vector=embedding, limit=1)
    if hits and hits[0].score >= threshold:
        payload = hits[0].payload
        return {
            "answer": payload["short_answer"],
            "steps": payload["canonical_solution_steps"],
            "solution": "\n".join(payload["canonical_solution_steps"]),
            "confidence": hits[0].score
        }
    return None
