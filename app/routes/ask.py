from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai import ask_question

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    context: str

@router.post("/api/ask")
def ask(req: AskRequest):
    answer = ask_question(req.question, req.context)
    if answer.startswith("Error:"):
        raise HTTPException(status_code=500, detail=answer)
    return {"answer": answer}
