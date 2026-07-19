from fastapi import FastAPI
from backend.app.api.document_routes import router as document_router

# إنشاء نسخة من تطبيق FastAPI
app = FastAPI(
    title="Qamar Tutor API",
    description="The production-ready backend API for Qamar Tutor AI assistant",
    version="0.1.0"
)

# تسجيل الـ Router الجديد في التطبيق الرئيسي مع إضافة v1 كمعيار لتنظيم إصدارات الـ API
app.include_router(document_router, prefix="/api/v1")

# أول Endpoint (Health Check)
@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "project": "Qamar Tutor",
        "message": "Welcome to Qamar Tutor AI Backend!"
    }