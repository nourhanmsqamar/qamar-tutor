from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from backend.app.models.user import User
from backend.app.core.security import get_current_user
# باقي الـ Imports الخاصة بـ Services بتاعتك زي GeminiService / PDFService لو موجودة
from backend.app.services.pdf_service import pdf_service  # 👈 استدعينا مطبخ الـ PDF

router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"]
)

# ... (الكود القديم بتاع /test و /ask-pdf سيبيه زي ما هو) ...

# 🚀 3. Integrated RAG Endpoint: Upload PDF & Ask Directly
@router.post("/ask-file")
async def ask_file(
    question: str = Form(...),          # استقبال السؤال
    file: UploadFile = File(...)        # استقبال ملف الـ PDF 
):
    """
    The Ultimate Pipeline: Uploads a PDF, extracts text on the fly,
    and feeds it into the RAG engine for an immediate answer.
    """
    # 1. التأكد إن الملف المرفوع PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        # 2. قراءة الملف من الريكويست
        file_bytes = await file.read()
        
        # 3. تقشير النص باستخدام الـ Service الجديدة
        extracted_text = pdf_service.extract_text_from_bytes(file_bytes)
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="The PDF appears to be empty or contains no readable text.")
        
        # 4. إرسال النص والسؤال لشيف الذكاء الاصطناعي
        ai_answer = gemini_service.ask_with_context(
            context=extracted_text, 
            question=question
        )
        
        return {
            "status": "success",
            "filename": file.filename,
            "question_asked": question,
            "ai_answer": ai_answer
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Pipeline Integration Error: {str(e)}"
        )

@router.post("/test")
def test_ai(prompt: str, current_user: User = Depends(get_current_user)):
    """إندبوينت محمي: لا يمكن استخدامه إلا بعد تسجيل الدخول"""
    return {
        "message": f"أهلاً بك يا {current_user.email}! تم التحقق من هويتك بنجاح.",
        "prompt_received": prompt
    }