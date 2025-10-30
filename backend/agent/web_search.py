import os
import requests
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Initialize Tavily client
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def query_ollama_mcp(question: str, context: str = "") -> dict:
    prompt = f"""
You are a math tutor. Answer the following question with a step-by-step solution.
Question: {question}
Context: {context}
Instructions: Use clear steps, simplify for a student.
"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma:2b", "prompt": prompt, "stream": False},
            timeout=30
        )
        result = response.json()
        answer_text = result.get("response", "").strip()

        return {
            "answer": answer_text,
            "steps": answer_text.split("\n"),
            "solution": answer_text,
            "confidence": 0.9
        }
    except Exception as e:
        raise RuntimeError(f"Ollama MCP failed: {str(e)}")

def package_mcp_context(question: str, retrieved_docs: list) -> str:
    system_instructions = (
        "You are a math tutor. Produce a step-by-step solution simplified for a high-school student. "
        "Cite sources. If content is not confirmed, return 'INSUFFICIENT_EXTERNAL_EVIDENCE'."
    )
    context_chunks = [
        f"Source: {doc['source']}\nContent: {doc['text']}\n"
        for doc in retrieved_docs
    ]
    context = "\n---\n".join(context_chunks)
    prompt = f"""
System Instructions:
{system_instructions}

User Question:
{question}

Retrieved Context:
{context}
"""
    return prompt.strip()

def search_web_and_generate(question: str) -> dict:
    try:
        results = client.search(query=question, max_results=5)
        docs = [{"source": r["url"], "text": r["content"]} for r in results]
        prompt = package_mcp_context(question, docs)
        return query_ollama_mcp(question, prompt)
    except Exception as e:
        return None  # Let routing fallback to MathSolver
