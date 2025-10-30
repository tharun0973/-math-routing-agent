from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import json, asyncio, traceback
from agent.routing import route_question

app = FastAPI(title="Math Routing Agent API", version="1.0.0")

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://localhost:5174",
        "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ✅ Request schema
class MathRequest(BaseModel):
    question: str
    stream: bool = False

# ✅ Response schema
class MathResponse(BaseModel):
    question: str
    answer: str
    steps: List[str]
    solution: str
    confidence: float

@app.get("/")
async def root():
    return {"status": "running", "message": "Math Routing Agent API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ✅ Main solve endpoint
@app.post("/solve", response_model=MathResponse)
async def solve_math(request: MathRequest):
    try:
        result = route_question(request.question)
        print("🔍 Routing result:", result)

        required_keys = ["answer", "steps", "solution", "confidence"]
        if not result or not all(k in result for k in required_keys):
            raise ValueError("Routing failed or incomplete result.")

        return MathResponse(
            question=request.question,
            answer=result["answer"],
            steps=result["steps"],
            solution=result["solution"],
            confidence=result["confidence"]
        )
    except Exception as e:
        print("❌ Error solving question:", request.question)
        print("🔧 Traceback:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error fetching answer.")

# ✅ Streaming endpoint (unchanged)
@app.post("/solve/stream")
async def solve_math_stream(request: MathRequest):
    async def generate():
        try:
            result = route_question(request.question)
            if result is None:
                yield json.dumps({"type": "error", "data": "Routing failed or no result returned."}) + "\n"
                return
            chunks = [
                json.dumps({"type": "question", "data": request.question}) + "\n",
                json.dumps({"type": "status", "data": "Solving..."}) + "\n"
            ]
            for i, step in enumerate(result["steps"], 1):
                chunks.append(json.dumps({"type": "step", "data": step, "number": i}) + "\n")
            chunks.append(json.dumps({"type": "solution", "data": result["solution"]}) + "\n")
            chunks.append(json.dumps({"type": "answer", "data": result["answer"]}) + "\n")
            chunks.append(json.dumps({"type": "done", "data": "Complete"}) + "\n")
            for chunk in chunks:
                yield chunk
                await asyncio.sleep(0.05)
        except Exception as e:
            print("Stream Error Traceback:", traceback.format_exc())
            yield json.dumps({"type": "error", "data": str(e)}) + "\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
