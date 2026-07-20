import fitz  # PyMuPDF
from fastapi import HTTPException

class PDFService:  # 👈 خلينا الحروف دي كلها كابيتال
    def extract_text_from_bytes(self, file_bytes: bytes) -> str:
        """
        Reads a PDF file from memory (bytes) and extracts all text.
        """
        try:
            pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
            extracted_text = ""
            
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                extracted_text += page.get_text("text") + "\n"
                
            pdf_document.close()
            return extracted_text.strip()
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to extract text from PDF: {str(e)}"
            )

# 👈 عملنا نسخة من الكلاس عشان الـ AI Router يستخدمها
pdf_service = PDFService()