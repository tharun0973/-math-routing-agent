import subprocess
from tavily import TavilyClient

client = TavilyClient(api_key="your_api_key")

def query_ollama_mcp(question: str, context: str = "") -> dict:
    prompt = f"""
You are a math tutor. Answer the following question with a step-by-step solution.
Question: {question}
Context: {context}
Instructions: Use clear steps, simplify for a student.
"""
    result = subprocess.run(
        ["ollama", "run", "gemma:2b"],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    output = result.stdout.decode("utf-8").strip()
    return {
        "answer": output,
        "steps": output.split("\n"),
        "solution": output,
        "confidence": 0.9
    }

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
    results = client.search(query=question, max_results=5)
    docs = [{"source": r["url"], "text": r["content"]} for r in results]
    prompt = package_mcp_context(question, docs)
    return query_ollama_mcp(question, prompt)
