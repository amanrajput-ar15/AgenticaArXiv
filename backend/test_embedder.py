import os
import shutil
from dotenv import load_dotenv  # <-- Add this import
from agenticarxiv.ingestion.embedder import Embedder
from agenticarxiv.vectorstore.faiss_store import FAISSStore

def run_day_2_test():
    print("Starting Day 2 Integration Test...\n")
    
    # Load the environment variables from .env
    load_dotenv()  # <-- Add this execution line
    
    # 1. Clean up any old test data
    if os.path.exists("agenticarxiv/embeddings"):
        shutil.rmtree("agenticarxiv/embeddings")
    
    # 2. Fake Data
    fake_chunks = [
        {"chunk_id": 0, "text": "The transformer architecture uses self-attention.", "title": "Attention Paper"},
        {"chunk_id": 1, "text": "FAISS is a library for efficient similarity search.", "title": "FAISS Paper"},
        {"chunk_id": 2, "text": "Langfuse provides observability for LLM applications.", "title": "Langfuse Paper"}
    ]
    
    try:
        # 3. Test Embedder
        print("Testing Embedder...")
        embedder = Embedder()
        embedded_chunks = embedder.embed_chunks(fake_chunks)
        print(f"✓ Generated {len(embedded_chunks)} embeddings.")
        
        # 4. Test FAISS Storage
        print("Testing FAISSStore...")
        vector_store = FAISSStore(dimension=768)
        vector_store.add_chunks(embedded_chunks)
        print(f"✓ Added chunks. ntotal: {vector_store.index.ntotal}")
        
        # 5. Test Retrieval
        print("Testing Retrieval...")
        query_vec = embedder.embed_text("How do I search efficiently?")
        results = vector_store.search(query_vec, k=1)
        print(f"✓ Top result: {results[0]['title']} (Distance: {results[0]['distance']:.4f})")
        
        # 6. Test Persistence
        print("Testing Save/Load...")
        vector_store.save()
        
        new_store = FAISSStore(dimension=768) # Should auto-load
        print(f"✓ Reloaded store. ntotal: {new_store.index.ntotal}")
        
        if new_store.index.ntotal == 3:
            print("\n🎉 ALL DAY 2 CHECKS PASSED!")
            
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")

if __name__ == "__main__":
    run_day_2_test()