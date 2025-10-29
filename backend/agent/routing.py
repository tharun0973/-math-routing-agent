from agent.knowledge_base import search_knowledge_base
from agent.web_search import search_web_and_generate, query_ollama_mcp
from agent.guardrails import validate_input, sanitize_output
from agent.math_solver import MathSolver
from agent.verifier import verify_answer

solver = MathSolver()

def route_question(question: str) -> dict:
    if not validate_input(question):
        return {
            "answer": "Invalid input. Please ask a math-related question.",
            "steps": [],
            "solution": "",
            "confidence": 0.0
        }

    kb_result = search_knowledge_base(question)
    if kb_result:
        return {
            "answer": kb_result["answer"],
            "steps": kb_result["steps"],
            "solution": kb_result["solution"],
            "confidence": 0.95
        }

    web_result = search_web_and_generate(question)
    if web_result:
        return {
            "answer": sanitize_output(web_result["answer"]),
            "steps": web_result["steps"],
            "solution": web_result["solution"],
            "confidence": 0.85
        }

    ollama_result = query_ollama_mcp(question)
    verified = verify_answer(question, ollama_result["answer"])

    return {
        "answer": sanitize_output(ollama_result["answer"]),
        "steps": ollama_result["steps"],
        "solution": ollama_result["solution"],
        "confidence": 0.9 if verified else 0.6
    }
