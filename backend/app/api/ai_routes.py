from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.services.gemini_service import gemini_service

router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"]
)

# 1. الموديل القديم للطلب التجريبي
class PromptRequest(BaseModel):
    prompt: str

@router.post("/test")
def test_gemini(request: PromptRequest):
    ai_response = gemini_service.generate_text(request.prompt)
    return {
        "status": "success",
        "prompt_sent": request.prompt,
        "response": ai_response
    }

# 2. 🚀 الموديل الجديد لجلسة RAG
class AskPdfRequest(BaseModel):
    document_text: str
    question: str

# 🛑 تأكدي من السطر ده بالظبط: مرري AskPdfRequest للدالة
@router.post("/ask-pdf")
def ask_pdf(request: AskPdfRequest): 
    """
    Accepts text extracted from a PDF and a question, 
    then returns an AI-generated answer based strictly on the text.
    """
    ai_answer = gemini_service.ask_with_context(
        context=request.document_text, 
        question=request.question
    )
    
    return {
        "status": "success",
        "question_asked": request.question,
        "ai_answer": ai_answer
    }