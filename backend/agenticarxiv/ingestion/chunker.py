from typing import List, Dict
import re

class Chunker:
    """Splits papers into semantic chunks for embedding and retrieval."""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        text = self._clean_text(text)
        words = text.split()
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(words):
            end = start + self.chunk_size
            chunk_words = words[start:end]
            chunk_text = ' '.join(chunk_words)
            
            chunk = {
                'chunk_id': chunk_id,
                'text': chunk_text,
                'paper_id': metadata.get('id'),
                'title': metadata.get('title'),
                'authors': metadata.get('authors'),
                'published': metadata.get('published'),
                'categories': metadata.get('categories'),
                'start_word': start,
                'end_word': end
            }
            chunks.append(chunk)
            
            chunk_id += 1
            start = end - self.overlap
            
            if end >= len(words):
                break
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def chunk_papers(self, papers: List[Dict]) -> List[Dict]:
        all_chunks = []
        for paper in papers:
            if 'text' not in paper:
                continue
            chunks = self.chunk_text(paper['text'], paper)
            all_chunks.extend(chunks)
        return all_chunks