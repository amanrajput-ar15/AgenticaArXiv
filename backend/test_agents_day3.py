import os
from dotenv import load_dotenv
import google.generativeai as genai
from agenticarxiv.agents.literature import LiteratureAgent
from agenticarxiv.agents.methods import MethodsAgent

def run_day_3_test():
    print("Starting Day 3 Diagnostics...\n")
    
    # 1. Auth check
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # 2. Fake RAG Context (Simulating FAISS output)
    fake_context = [
        {
            "paper_id": "2026.001",
            "title": "Attention is All You Need",
            "authors": ["Vaswani", "Shazeer"],
            "published": "2017-06-12",
            "text": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. The method uses multi-head self-attention."
        },
        {
            "paper_id": "2026.002",
            "title": "BERT: Pre-training of Deep Bidirectional Transformers",
            "authors": ["Devlin", "Chang"],
            "published": "2018-10-11",
            "text": "Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers."
        }
    ]
    
    query = "How did transformer architectures evolve from 2017 to 2018?"
    
    try:
        # Test Literature Agent
        print("Testing Literature Agent...")
        lit_agent = LiteratureAgent()
        lit_result = lit_agent.execute(query, fake_context)
        print(f"✓ Success! Literature analysis length: {len(lit_result['analysis'])} characters")
        print(f"✓ Agent tag: {lit_result['agent']}")
        print(f"✓ Sources used: {lit_result['sources_used']}\n")
        
        # Test Methods Agent
        print("Testing Methods Agent...")
        methods_agent = MethodsAgent()
        methods_result = methods_agent.execute(query, fake_context)
        print(f"✓ Success! Methods analysis length: {len(methods_result['analysis'])} characters")
        print(f"✓ Agent tag: {methods_result['agent']}")
        print(f"✓ Sources used: {methods_result['sources_used']}")
        
        print("\n🎉 ALL DAY 3 CHECKS PASSED!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")

if __name__ == "__main__":
    run_day_3_test()