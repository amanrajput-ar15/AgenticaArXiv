import os
import sys
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

def run_diagnostics():
    print("Starting Day 1 Diagnostics...\n")

    # Check 1: API Key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_key_here":
        print("[KEY]   ❌ GEMINI_API_KEY not found or invalid in .env")
        sys.exit(1)
    print("[KEY]   ✓ GEMINI_API_KEY found")

    # Configure SDK
    genai.configure(api_key=api_key)

    # Check 2: LLM Generation (Updated to 2.5 Flash)
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content("Reply with exactly one word: Hello")
        print(f"[LLM]   ✓ gemini-2.5-flash responded: {response.text.strip()}")
    except Exception as e:
        print(f"[LLM]   ❌ LLM generation failed: {e}")
        sys.exit(1)

    # Check 3: Embedding Shape (Updated to Embedding 2 with 768-dim scaling)
    try:
        result = genai.embed_content(
            model="models/gemini-embedding-2-preview",
            content="This is a test document to verify our embedding vector dimensions.",
            task_type="retrieval_document",
            output_dimensionality=768  # <-- CRITICAL: Forces 768 dimensions for FAISS
        )
        embedding = np.array(result["embedding"], dtype="float32")
        print(f"[EMBED] ✓ shape: {embedding.shape}  dtype: {embedding.dtype}")

        if embedding.shape != (768,):
            print(f"[EMBED] ❌ CRITICAL WARNING: Expected shape (768,), got {embedding.shape}")
            sys.exit(1)
            
    except Exception as e:
        print(f"[EMBED] ❌ Embedding generation failed: {e}")
        sys.exit(1)

    print("\n✓ All Day 1 checks passed. You are cleared for Day 2.")

if __name__ == "__main__":
    run_diagnostics()