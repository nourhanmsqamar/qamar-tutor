import pypdf
from fastapi import HTTPException

class PDFService:
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Takes a local PDF file path, extracts all available text, 
        and returns it as a single concatenated string.
        """
        try:
            extracted_text = ""
            
            # 1. Open and read the PDF file
            with open(file_path, "rb") as file:
                reader = pypdf.PdfReader(file)
                
                # 2. Loop through every page and extract text
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"
            
            # 3. Check if we actually found any text
            if not extracted_text.strip():
                raise HTTPException(
                    status_code=400, 
                    detail="The uploaded PDF appears to be empty or scanned (images only). Qamar Tutor currently supports text-based PDFs."
                )
                
            return extracted_text
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"An error occurred while processing the PDF: {str(e)}"
            )