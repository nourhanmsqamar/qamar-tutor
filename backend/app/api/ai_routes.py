from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.services.gemini_service import gemini_service

# 1. إنشاء Router مخصص لعمليات الذكاء الاصطناعي
router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"]
)

# 2. تحديد هيكل البيانات القادمة من الـ Frontend
class PromptRequest(BaseModel):
    prompt: str

# 3. إنشاء الـ Endpoint وتوصيلها بالشيف
@router.post("/test")
def test_gemini(request: PromptRequest):
    """
    Accepts a raw text prompt, sends it to Gemini Service, 
    and returns the fully generated AI response.
    """
    # نأخذ الـ prompt ونمرره للشيف عشان يكلم جوجل جيميني
    ai_response = gemini_service.generate_text(request.prompt)
    
    # السطر السحري الناقص: إرجاع النتيجة للـ Swagger UI
    return {
        "status": "success",
        "prompt_sent": request.prompt,
        "response": ai_response
    }