import chromadb
from backend.app.core.config import settings
from .embedding_service import embedding_service
from typing import List, Dict

class VectorStoreService:
    def __init__(self):
        # Initialize ChromaDB persistent client
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
        # Create or load the collection
        self.collection = self.client.get_or_create_collection(name=settings.CHROMA_COLLECTION_NAME)
        
    def store_chunks(self, chunks: List[Dict], document_id: int, user_id: int, filename: str):
        """
        Generates embeddings and stores chunks alongside their metadata in ChromaDB.
        Expects chunks in format: [{"index": int, "content": str}]
        """
        if not chunks:
            return
            
        texts = [chunk["content"] for chunk in chunks]
        
        # 1. Generate Embeddings using our EmbeddingService
        embeddings = embedding_service.generate_embeddings(texts)
        
        # 2. Prepare data for ChromaDB
        ids = []
        metadatas = []
        
        for chunk in chunks:
            # Create a unique ID for each chunk
            chunk_id = f"doc_{document_id}_chunk_{chunk['index']}"
            ids.append(chunk_id)
            
            # Store required metadata
            metadata = {
                "document_id": document_id,
                "user_id": user_id,
                "chunk_index": chunk['index'],
                "filename": filename
            }
            metadatas.append(metadata)
            
        # 3. Store in the collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts
        )

    def search(self, query: str, user_id: int, document_id: int = None, top_k: int = 5) -> List[Dict]:
        """
        Searches ChromaDB for the most relevant chunks using semantic search.
        Returns a list of dicts: {"content": str, "metadata": dict, "distance": float}
        """
        # 1. Generate query embedding
        query_embedding = embedding_service.generate_embeddings([query])[0]
        
        # 2. Build where filter
        where_filter = {"user_id": user_id}
        if document_id is not None:
            where_filter = {
                "$and": [
                    {"user_id": user_id},
                    {"document_id": document_id}
                ]
            }
            
        # 3. Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
        
        # 4. Format results
        parsed_results = []
        if results and results.get('documents') and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                parsed_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if results.get('distances') else None
                })
                
        return parsed_results

vector_store_service = VectorStoreService()
