import os
import time
from typing import List, Dict
import numpy as np
import google.generativeai as genai

class Embedder:
    """Generates embeddings for text chunks using Gemini."""
    
    def __init__(self, model: str = "models/gemini-embedding-2-preview"):
        self.model = model
        self.dimension = 768
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)
    
    def embed_text(self, text: str, task_type: str = "retrieval_query") -> np.ndarray:
        """
        Generate embedding for a single text (usually a user query).
        """
        result = genai.embed_content(
            model=self.model,
            content=text,
            task_type=task_type,
            output_dimensionality=self.dimension
        )
        return np.array(result["embedding"], dtype="float32")
    
    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Generate embeddings for multiple chunks in batches to respect rate limits.
        """
        batch_size = 100
        
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            texts = [chunk['text'] for chunk in batch_chunks]
            
            # Use 'retrieval_document' when storing chunks in the database
            response = genai.embed_content(
                model=self.model,
                content=texts,
                task_type="retrieval_document",
                output_dimensionality=self.dimension
            )
            
            for j, chunk in enumerate(batch_chunks):
                chunk['embedding'] = np.array(response['embedding'][j], dtype="float32")
                
            # Sleep briefly to avoid hitting the 1500 req/min free tier limit
            if i + batch_size < len(chunks):
                time.sleep(0.5)
                
        return chunks