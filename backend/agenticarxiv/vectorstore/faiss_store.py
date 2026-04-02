import os
import pickle
import numpy as np
import faiss
from typing import List, Dict

class FAISSStore:
    """Vector database using FAISS for efficient similarity search."""
    
    def __init__(self, dimension: int = 768, index_path: str = "agenticarxiv/embeddings/faiss.index"):
        self.dimension = dimension
        self.index_path = index_path
        self.metadata_path = index_path.replace('.index', '_metadata.pkl')
        
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        if os.path.exists(index_path) and os.path.exists(self.metadata_path):
            self.load()
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata: List[Dict] = []
    
    def add_chunks(self, chunks: List[Dict]) -> None:
        if not chunks:
            return

        embeddings = np.array([chunk['embedding'] for chunk in chunks], dtype="float32")
        
        # GUARD 1: Prevent silent garbage data ingestion
        if embeddings.shape[1] != self.dimension:
            raise ValueError(
                f"Dimension mismatch: chunks are {embeddings.shape[1]}-dim, "
                f"index expects {self.dimension}-dim."
            )
        
        self.index.add(embeddings)
        
        for chunk in chunks:
            self.metadata.append({k: v for k, v in chunk.items() if k != 'embedding'})
            
        # GUARD 2: The Sync Contract. If this fails, the DB is corrupt.
        assert self.index.ntotal == len(self.metadata), (
            f"SYNC BROKEN: index.ntotal={self.index.ntotal}, len(metadata)={len(self.metadata)}"
        )
    
    def search(self, query_embedding: np.ndarray, k: int = 10) -> List[Dict]:
        if self.index.ntotal == 0:
            return []
            
        k = min(k, self.index.ntotal)
        query_vector = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1 or idx >= len(self.metadata):
                continue
            result = self.metadata[idx].copy()
            result['distance'] = float(dist)
            results.append(result)
            
        return results
    
    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
    
    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)
            
        # GUARD 3: Ensure files loaded from disk aren't desynced
        assert self.index.ntotal == len(self.metadata), (
            f"LOAD ERROR: index={self.index.ntotal} != metadata={len(self.metadata)}. "
            f"Clear the embeddings/ directory and re-ingest."
        )
    
    def clear(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        
    def get_stats(self) -> Dict:
        size_mb = os.path.getsize(self.index_path) / (1024 * 1024) if os.path.exists(self.index_path) else 0
        return {
            'total_chunks': self.index.ntotal,
            'dimension': self.dimension,
            'index_size_mb': round(size_mb, 2)
        }