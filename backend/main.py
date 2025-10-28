"""
Math Routing Agent - FastAPI Backend
Core API with SymPy integration for math problem solving
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import json
import time
import asyncio

from math_solver import MathSolver

app = FastAPI(
    title="Math Routing Agent API",
    description="AI-powered mathematics assistant backend",
    version="1.0.0"
)

# CORS Configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize math solver
solver = MathSolver()


class MathRequest(BaseModel):
    question: str
    stream: bool = False


class MathResponse(BaseModel):
    question: str
    answer: str
    steps: List[str]
    solution: str
    confidence: float


@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "Math Routing Agent API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/solve", response_model=MathResponse)
async def solve_math(request: MathRequest):
    """
    Solve a math problem and return structured response
    """
    try:
        # Solve the math problem
        result = solver.solve(request.question)
        
        return MathResponse(
            question=request.question,
            answer=result["answer"],
            steps=result["steps"],
            solution=result["solution"],
            confidence=result["confidence"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error solving problem: {str(e)}")


@app.post("/solve/stream")
async def solve_math_stream(request: MathRequest):
    """
    Solve a math problem with streaming response
    """
    async def generate():
        try:
            # Solve the problem
            result = solver.solve(request.question)
            
            # Stream the response
            chunks = [
                json.dumps({"type": "question", "data": request.question}) + "\n",
                json.dumps({"type": "status", "data": "Solving..."}) + "\n",
            ]
            
            # Stream steps
            for i, step in enumerate(result["steps"], 1):
                chunks.append(
                    json.dumps({"type": "step", "data": step, "number": i}) + "\n"
                )
            
            # Stream solution
            chunks.append(
                json.dumps({"type": "solution", "data": result["solution"]}) + "\n"
            )
            
            chunks.append(
                json.dumps({"type": "answer", "data": result["answer"]}) + "\n"
            )
            
            chunks.append(
                json.dumps({"type": "done", "data": "Complete"}) + "\n"
            )
            
            # Yield chunks with delay for streaming effect
            for chunk in chunks:
                yield chunk
                await asyncio.sleep(0.05)  # Small delay for streaming effect
                
        except Exception as e:
            error_chunk = json.dumps({"type": "error", "data": str(e)}) + "\n"
            yield error_chunk
    
    return StreamingResponse(generate(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

