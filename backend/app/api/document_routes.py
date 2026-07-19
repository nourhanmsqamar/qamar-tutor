import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.services.pdf_service import PDFService

# 1. إنشاء Router مخصص لملفات المستندات
router = APIRouter(
    prefix="/docs",
    tags=["Documents"]
)

# فولدر مؤقت لحفظ الملفات المرفوعة
UPLOAD_DIR = "backend/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 2. إنشاء الـ Endpoint الخاصة برفع الـ PDF واستخراج النص
@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # حماية هندسية: التأكد إن الملف المرفوع هو PDF فعلاً
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only PDF files are supported."
        )
    
    # مسار الحفظ المؤقت للملف
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # 3. حفظ ملف الـ Binary القادم من الـ Frontend إلى الهارد ديسك
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 4. إرسال المسار للشيف (PDFService) لاستخراج النص
        extracted_text = PDFService.extract_text_from_pdf(file_path)
        
        # 5. إرجاع النتيجة للـ Frontend
        return {
            "filename": file.filename,
            "status": "success",
            "extracted_text_length": len(extracted_text),
            "content": extracted_text
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # تنظيف السيرفر: مسح الملف بعد استخراج النص عشان ميملاش الهارد ديسك
        if os.path.exists(file_path):
            os.remove(file_path)