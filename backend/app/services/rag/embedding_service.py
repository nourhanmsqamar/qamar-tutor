from sentence_transformers import SentenceTransformer
from backend.app.core.config import settings

class EmbeddingService:
    def __init__(self):
        # We load the model once when the service is instantiated
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        
    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generates embeddings for a list of texts.
        Returns a list of float arrays (embeddings).
        """
        if not texts:
            return []
            
        # encode() returns a numpy array by default
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

embedding_service = EmbeddingService()
