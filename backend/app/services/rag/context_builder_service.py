from typing import List, Dict

class ContextBuilderService:
    @staticmethod
    def build_context(retrieved_chunks: List[Dict], max_chars: int) -> str:
        """
        Builds the context string from retrieved chunks.
        Sorts chunks by their original index to preserve reading order.
        Respects the max_chars limit to avoid LLM context bloat.
        """
        if not retrieved_chunks:
            return ""
            
        # 1. Deduplicate by chunk_index to avoid passing redundant info to the AI
        unique_chunks = {}
        for chunk in retrieved_chunks:
            idx = chunk["metadata"].get("chunk_index", 0)
            if idx not in unique_chunks:
                unique_chunks[idx] = chunk["content"]
                
        # 2. Sort chunks by chunk_index to preserve semantic reading order
        sorted_indices = sorted(unique_chunks.keys())
        
        # 3. Build the final context string without exceeding max_chars
        context_parts = []
        current_length = 0
        
        for idx in sorted_indices:
            content = unique_chunks[idx]
            
            # Check if adding this chunk exceeds the max length
            # (+2 for the newline separators)
            if current_length + len(content) + 2 > max_chars:
                # If we haven't added anything yet, truncate this chunk so the AI gets at least some context
                if not context_parts:
                    remaining_space = max_chars - current_length
                    context_parts.append(content[:remaining_space])
                # Otherwise, just break to ensure we only send clean, complete chunks
                break
                
            context_parts.append(content)
            current_length += len(content) + 2
            
        return "\n\n".join(context_parts)

context_builder_service = ContextBuilderService()
