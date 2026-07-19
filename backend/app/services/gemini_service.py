from groq import Groq
from fastapi import HTTPException
from backend.app.core.config import settings

class GeminiService:  # حافظنا على اسم الكلاس عشان الـ Imports بره متتكسرش
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in the environment or .env file.")
        
        # تشغيل Client شركة Groq بدلاً من جوجل
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    def generate_text(self, prompt: str) -> str:
        try:
            # إرسال الطلب لـ Groq API بنظام الشات القياسي
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
            )
            
            # استخراج النص الراجع بنجاح
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Groq API Error: {str(e)}"
            )

gemini_service = GeminiService()