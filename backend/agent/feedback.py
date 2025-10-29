from agent.dspy_agent import MathFeedbackAgent

agent = MathFeedbackAgent()

def refine_with_feedback(question: str, rating: int, comment: str = "") -> dict:
    if rating < 3:
        improved = agent.forward(question)
        return {
            "status": "refined",
            "answer": improved.answer,
            "steps": improved.steps,
            "solution": improved.solution
        }
    return {"status": "no_change", "message": "High rating — no refinement needed."}
