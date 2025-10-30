from sympy import symbols, Eq, solve, simplify
from sympy.parsing.sympy_parser import parse_expr

class MathSolver:
    def __init__(self):
        self.x = symbols('x')

    def solve_equation(self, question: str):
        try:
            # Convert equation to expression: "x^2 + 5x + 6 = 0" → "x^2 + 5x + 6 - (0)"
            expr = parse_expr(question.replace('=', '-(') + ')')
            simplified = simplify(expr)
            solutions = solve(simplified, self.x)
            steps = [
                f"Parsed expression: {expr}",
                f"Simplified: {simplified}",
                f"Solved: {solutions}"
            ]
            solution_latex = f"${question} \\Rightarrow {simplified}$"
            return {
                "answer": ", ".join([str(s) for s in solutions]),
                "steps": steps,
                "solution": solution_latex,
                "confidence": 0.95
            }
        except Exception as e:
            return {
                "answer": "Error",
                "steps": [str(e)],
                "solution": "Could not solve",
                "confidence": 0.0
            }
