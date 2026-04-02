import os
from dotenv import load_dotenv
import google.generativeai as genai

from agenticarxiv.agents.literature import LiteratureAgent
from agenticarxiv.agents.methods import MethodsAgent
from agenticarxiv.agents.results import ResultsAgent
from agenticarxiv.agents.critique import CritiqueAgent
from agenticarxiv.agents.synthesis import SynthesisAgent

def run_day_4_test():
    print("Starting Day 4 Diagnostics (All 5 Agents)...\n")
    
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    fake_context = [
        {
            "paper_id": "2026.001",
            "title": "Attention is All You Need",
            "authors": ["Vaswani", "Shazeer"],
            "published": "2017-06-12",
            "text": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. The method uses multi-head self-attention. Results show 28.4 BLEU on English-to-German. A limitation is the quadratic complexity of self-attention."
        },
        {
            "paper_id": "2026.002",
            "title": "BERT: Pre-training of Deep Bidirectional Transformers",
            "authors": ["Devlin", "Chang"],
            "published": "2018-10-11",
            "text": "Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. It achieves 93.3% accuracy on SQuAD."
        }
    ]
    
    query = "How did transformer architectures evolve from 2017 to 2018, what were their limitations, and what were the performance improvements?"
    
    agents = [
        ("Literature", LiteratureAgent()),
        ("Methods", MethodsAgent()),
        ("Results", ResultsAgent()),
        ("Critique", CritiqueAgent()),
        ("Synthesis", SynthesisAgent())
    ]
    
    try:
        for name, agent in agents:
            print(f"Testing {name} Agent...")
            result = agent.execute(query, fake_context)
            print(f"  ✓ Tag: {result['agent']}")
            print(f"  ✓ Output: {len(result['analysis'])} chars")
            
        print("\n🎉 ALL DAY 4 CHECKS PASSED!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")

if __name__ == "__main__":
    run_day_4_test()