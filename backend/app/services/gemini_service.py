from groq import Groq
from fastapi import HTTPException
from backend.app.core.config import settings

class GeminiService:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in the environment or .env file.")
        
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    # الدالة القديمة بتاعة الجلسة الرابعة (سؤال عام)
    def generate_text(self, prompt: str) -> str:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Groq API Error: {str(e)}")

    # 🚀 الدالة الجديدة بتاعة الجلسة الخامسة (سؤال من الـ PDF)
    def ask_with_context(self, context: str, question: str) -> str:
        """
        Takes extracted PDF text (context) and a user question, 
        forces the AI to answer ONLY from the provided text.
        """
        # الـ System Prompt: دي التعليمات الصارمة اللي بنديها للذكاء الاصطناعي عشان ميهلوسش
        system_instruction = (
            "You are a helpful and smart AI Tutor named 'Qamar'. "
            "You must answer the user's question strictly based on the provided text context. "
            "If the answer is NOT in the context, clearly state: 'I don't know based on the provided document.'"
        )
        
        # دمج النص المستخرج مع سؤال الطالب
        combined_prompt = f"Context (PDF Text):\n{context}\n\nQuestion:\n{question}"
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": combined_prompt}
                ],
                model=self.model,
            )
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Groq API Context Error: {str(e)}"
            )

gemini_service = GeminiService()