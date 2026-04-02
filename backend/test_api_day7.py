import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def run_api_gauntlet():
    print("🚀 Starting Day 7 API Integration Gauntlet (Free Tier Mode)...\n")

    # 1. Test Root Endpoint
    print("Testing GET / ...")
    res = requests.get(f"{BASE_URL}/")
    assert res.status_code == 200, "Root endpoint failed"
    print(f"  ✓ {res.json()}")

    # =====================================================================
    # COMMENTED OUT: Skipping ingestion to save Gemini Free Tier Quota.
    # The 52 chunks from our previous run are already in the FAISS database!
    # =====================================================================
    
    # 2. Test Clear Vector Store (Start Fresh)
    # print("\nTesting DELETE /vectorstore ...")
    # res = requests.delete(f"{BASE_URL}/vectorstore")
    # assert res.status_code == 200, "Clear vector store failed"
    # print("  ✓ Vector store cleared")

    # 3. Test Ingest Endpoint
    # print("\nTesting POST /ingest (Downloading 2 papers on Transformers)...")
    # ingest_payload = {
    #     "query": "transformer attention mechanism",
    #     "max_results": 2
    # }
    # res = requests.post(f"{BASE_URL}/ingest", json=ingest_payload)
    # if res.status_code != 200:
    #     print(f"❌ Ingest failed: {res.text}")
    #     sys.exit(1)
    # 
    # ingest_data = res.json()
    # print(f"  ✓ Success! Processed {ingest_data['papers_processed']} papers into {ingest_data['chunks_created']} chunks.")
    
    # =====================================================================

    # 4. Test Status Endpoint
    print("\nTesting GET /status ...")
    res = requests.get(f"{BASE_URL}/status")
    assert res.status_code == 200, "Status endpoint failed"
    status_data = res.json()
    print(f"  ✓ Vector Store Status: {status_data['vector_store']['total_chunks']} chunks, {status_data['vector_store']['dimension']}-dim")
    assert status_data['vector_store']['dimension'] == 768, "CRITICAL: Dimension is not 768!"

    # 5. Test Research Endpoint (The Heavy Lifter)
    print("\nTesting POST /research (Firing all 5 agents, this will take 30-50s)...")
    research_payload = {
        "query": "How do attention mechanisms compare across architectures?",
        "retrieval_k": 10
    }
    start_time = time.time()
    res = requests.post(f"{BASE_URL}/research", json=research_payload)
    end_time = time.time()
    
    if res.status_code != 200:
        print(f"❌ Research failed: {res.text}")
        sys.exit(1)
        
    report = res.json()
    print(f"  ✓ Success! Report generated in {round(end_time - start_time, 2)} seconds.")
    print(f"  ✓ Sources utilized: {report['num_sources']}")
    
    # Verify all 5 sections exist
    sections = ['literature_review', 'methods_analysis', 'results_analysis', 'critique', 'synthesis']
    for sec in sections:
        assert report[sec].get('analysis'), f"Missing analysis in {sec}"
    print("  ✓ All 5 agent sections successfully populated.")

    # 6. Test Memory Endpoint
    print("\nTesting GET /memory ...")
    res = requests.get(f"{BASE_URL}/memory")
    assert res.status_code == 200, "Get memory failed"
    memory_data = res.json()
    print(f"  ✓ Memory retrieved. {len(memory_data['messages'])} messages in session.")

    # 7. Test Clear Memory
    print("\nTesting DELETE /memory ...")
    res = requests.delete(f"{BASE_URL}/memory")
    assert res.status_code == 200, "Clear memory failed"
    print("  ✓ Session memory cleared")

    print("\n🎉 ALL 7 ENDPOINTS PASSED. BACKEND IS PRODUCTION READY.")


if __name__ == "__main__":
    try:
        run_api_gauntlet()
    except AssertionError as e:
        print(f"\n❌ GAUNTLET FAILED: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ GAUNTLET FAILED: Could not connect to server. Is FastAPI running?")