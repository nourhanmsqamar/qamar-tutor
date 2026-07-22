import re

class PreprocessingService:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans and normalizes extracted PDF text.
        Preserves English and Arabic text.
        """
        # Normalize line breaks
        text = text.replace('\r\n', '\n')
        
        # Preserve paragraph boundaries by temporarily replacing \n\n or more with a token
        text = re.sub(r'\n{2,}', '<PARAGRAPH_BREAK>', text)
        
        # Replace remaining single \n with a space (removes arbitrary line breaks within sentences)
        text = text.replace('\n', ' ')
        
        # Replace special token back to \n\n
        text = text.replace('<PARAGRAPH_BREAK>', '\n\n')
        
        # Remove multiple spaces/tabs
        text = re.sub(r'[ \t]+', ' ', text)
        
        return text.strip()

preprocessing_service = PreprocessingService()
