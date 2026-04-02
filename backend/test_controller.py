import os
from dotenv import load_dotenv
from agenticarxiv.ingestion.arxiv_loader import ArxivLoader
from agenticarxiv.ingestion.pdf_parser import PDFParser
from agenticarxiv.ingestion.chunker import Chunker
from agenticarxiv.ingestion.embedder import Embedder
from agenticarxiv.vectorstore.faiss_store import FAISSStore
from agenticarxiv.mcp.controller import MCPController
from agenticarxiv.agents.literature import LiteratureAgent
from agenticarxiv.agents.methods import MethodsAgent
from agenticarxiv.agents.results import ResultsAgent
from agenticarxiv.agents.critique import CritiqueAgent
from agenticarxiv.agents.synthesis import SynthesisAgent

def run_day_5_test():
    print("Starting Day 5 Diagnostics: Full End-to-End Orchestration...\n")
    load_dotenv()
    
    try:
        # 1. Ingest a real paper
        print("Ingesting test paper from arXiv...")
        loader = ArxivLoader()
        papers = loader.search("attention is all you need", max_results=1)
        papers = loader.download_papers(papers)
        papers = PDFParser().parse_papers(papers)
        chunks = Chunker().chunk_papers(papers)
        
        embedder = Embedder()
        chunks = embedder.embed_chunks(chunks)
        
        vector_store = FAISSStore(dimension=768)
        vector_store.clear() # Start fresh
        vector_store.add_chunks(chunks)
        vector_store.save()
        print(f"✓ Ingested {len(chunks)} chunks into FAISS.")

        # 2. Setup Controller
        print("\nInitializing MCP Controller...")
        controller = MCPController(vector_store, embedder)
        controller.register_agent('literature', LiteratureAgent())
        controller.register_agent('methods', MethodsAgent())
        controller.register_agent('results', ResultsAgent())
        controller.register_agent('critique', CritiqueAgent())
        controller.register_agent('synthesis', SynthesisAgent())
        
        # 3. Run Orchestration
        query = "What is the core mechanism proposed in this paper?"
        print(f"Executing Query: '{query}'")
        report = controller.orchestrate(query, retrieval_k=5)
        
        # 4. Verify Output
        print("\nVerifying Report Sections...")
        sections = ['literature_review', 'methods_analysis', 'results_analysis', 'critique', 'synthesis']
        for sec in sections:
            if report.get(sec, {}).get('analysis'):
                print(f"  ✓ {sec} generated successfully.")
            else:
                raise ValueError(f"Missing analysis in {sec}")
                
        print(f"  ✓ Sources utilized: {report['num_sources']}")
        print("\n🎉 ALL DAY 5 CHECKS PASSED! BACKEND IS COMPLETE.")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")

if __name__ == "__main__":
    run_day_5_test()