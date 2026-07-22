import re
from typing import List, Dict

class ChunkingService:
    @staticmethod
    def chunk_text(text: str, max_chunk_size: int, overlap: int) -> List[Dict]:
        """
        Splits text into chunks of roughly max_chunk_size characters, with an overlap.
        Returns a list of dictionaries with metadata: {"index": int, "content": str}
        """
        # Split by paragraph boundaries first
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        chunk_index = 0
        
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
                
            # If a single paragraph is larger than max_chunk_size, we need to split it by sentences
            if len(p) > max_chunk_size:
                # Split by sentence boundaries (. ! ? ؟)
                sentences = re.split(r'(?<=[.!?؟])\s+', p)
                for sentence in sentences:
                    if not sentence:
                        continue
                    
                    if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
                        current_chunk += (" " + sentence if current_chunk else sentence)
                    else:
                        if current_chunk:
                            chunks.append({"index": chunk_index, "content": current_chunk.strip()})
                            chunk_index += 1
                            
                            # Create overlap
                            overlap_text = current_chunk[-overlap:] if overlap < len(current_chunk) else current_chunk
                            # Try to start overlap at a word boundary
                            overlap_start = overlap_text.find(' ')
                            if overlap_start != -1 and overlap_start < len(overlap_text) - 1:
                                overlap_text = overlap_text[overlap_start + 1:]
                            
                            current_chunk = overlap_text + " " + sentence if overlap_text else sentence
                        else:
                            # Sentence itself is larger than max_chunk_size, force split by characters
                            for i in range(0, len(sentence), max_chunk_size - overlap):
                                part = sentence[i:i + max_chunk_size]
                                chunks.append({"index": chunk_index, "content": part.strip()})
                                chunk_index += 1
                            current_chunk = ""
                            
            else:
                # Normal paragraph size
                if len(current_chunk) + len(p) + 2 <= max_chunk_size:
                    current_chunk += ("\n\n" + p if current_chunk else p)
                else:
                    if current_chunk:
                        chunks.append({"index": chunk_index, "content": current_chunk.strip()})
                        chunk_index += 1
                        
                        # Create overlap
                        overlap_text = current_chunk[-overlap:] if overlap < len(current_chunk) else current_chunk
                        overlap_start = overlap_text.find(' ')
                        if overlap_start != -1 and overlap_start < len(overlap_text) - 1:
                            overlap_text = overlap_text[overlap_start + 1:]
                        
                        current_chunk = overlap_text + "\n\n" + p if overlap_text else p
                    else:
                        current_chunk = p
                        
        if current_chunk:
            chunks.append({"index": chunk_index, "content": current_chunk.strip()})
            
        return chunks

chunking_service = ChunkingService()
