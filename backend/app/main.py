from fastapi import FastAPI

# 1. إنشاء نسخة من تطبيق FastAPI
app = FastAPI(
    title="Qamar Tutor API",
    description="The production-ready backend API for Qamar Tutor AI assistant",
    version="0.1.0"
)

# 2. إنشاء أول Endpoint (Health Check)
@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "project": "Qamar Tutor",
        "message": "Welcome to Qamar Tutor AI Backend!"
    }