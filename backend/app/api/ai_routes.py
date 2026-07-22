from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.core.security import get_current_user
from backend.app.services.pdf_service import pdf_service
from backend.app.services.gemini_service import gemini_service
from backend.app.services.chat_service import chat_service
from backend.app.core.config import settings
from backend.app.services.rag import preprocessing_service, chunking_service, vector_store_service, context_builder_service

router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"]
)

# ... (الكود القديم بتاع /test و /ask-pdf سيبيه زي ما هو) ...

# 🚀 3. Integrated RAG Endpoint: Upload PDF & Ask Directly
@router.post("/ask-file")
async def ask_file(
    question: str = Form(...),          # استقبال السؤال
    file: UploadFile = File(...),       # استقبال ملف الـ PDF 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
        
        # 4. Create Document record
        document = chat_service.create_document(
            db=db,
            user_id=current_user.id,
            filename=file.filename,
            original_filename=file.filename
        )
        
        # 5. Create Chat Session
        session = chat_service.get_or_create_session(
            db=db,
            user_id=current_user.id,
            document_id=document.id
        )
        
        # 6. Save user question
        chat_service.save_message(
            db=db,
            session_id=session.id,
            role="user",
            content=question
        )

        # --- NEW RAG PHASE 1 ---
        cleaned_text = preprocessing_service.clean_text(extracted_text)
        chunks = chunking_service.chunk_text(
            text=cleaned_text,
            max_chunk_size=settings.RAG_CHUNK_SIZE,
            overlap=settings.RAG_CHUNK_OVERLAP
        )
        # --- NEW RAG PHASE 2 (Indexing) ---
        vector_store_service.store_chunks(
            chunks=chunks,
            document_id=document.id,
            user_id=current_user.id,
            filename=file.filename
        )
        
        # --- NEW RAG PHASE 3 (Retrieval & Context Building) ---
        retrieved_chunks = vector_store_service.search(
            query=question,
            user_id=current_user.id,
            document_id=document.id,
            top_k=settings.RAG_TOP_K
        )
        
        rag_context = context_builder_service.build_context(
            retrieved_chunks=retrieved_chunks,
            max_chars=settings.MAX_CONTEXT_CHARS
        )
        
        # 7. إرسال النص والسؤال لشيف الذكاء الاصطناعي
        ai_answer = gemini_service.ask_with_context(
            context=rag_context, 
            question=question
        )
        
        # 8. Save assistant answer
        chat_service.save_message(
            db=db,
            session_id=session.id,
            role="assistant",
            content=ai_answer
        )
        
        return {
            "status": "success",
            "filename": file.filename,
            "session_id": session.id,
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