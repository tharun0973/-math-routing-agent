import os
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, PointStruct, SearchParams
from qdrant_client.http.models import SearchRequest, VectorParams
import requests
from dotenv import load_dotenv

load_dotenv()

# Initialize Qdrant client
client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

def generate_embedding(text: str) -> list:
    try:
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": "gemma:2b", "prompt": text},
            timeout=30
        )
        result = response.json()
        return result.get("embedding", [])
    except Exception as e:
        raise RuntimeError(f"Embedding generation failed: {str(e)}")

def search_knowledge_base(question: str) -> dict:
    embedding = generate_embedding(question)
    try:
        hits = client.search(
            collection_name="math_kb",
            query_vector=embedding,
            limit=1,
            search_params=SearchParams(hnsw_ef=128)
        )
        if not hits:
            return None
        top_hit = hits[0]
        return {
            "answer": top_hit.payload.get("answer", ""),
            "steps": top_hit.payload.get("steps", "").split("\n"),
            "solution": top_hit.payload.get("solution", ""),
            "confidence": top_hit.score
        }
    except Exception as e:
        raise RuntimeError(f"Qdrant search failed: {str(e)}")
