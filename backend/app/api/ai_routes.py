from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from backend.app.services.gemini_service import gemini_service
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