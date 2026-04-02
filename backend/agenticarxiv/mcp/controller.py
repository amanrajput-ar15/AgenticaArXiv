import os
from typing import List, Dict, Any
import google.generativeai as genai
from langfuse import Langfuse
from agenticarxiv.mcp.memory import Memory
from agenticarxiv.vectorstore.faiss_store import FAISSStore
from agenticarxiv.ingestion.embedder import Embedder

class MCPController:
    """Multi-agent controller orchestrating specialized research agents."""
    
    def __init__(
        self,
        vector_store: FAISSStore,
        embedder: Embedder,
        llm_model: str = "gemini-2.5-flash", # Updated to the active model
    ) -> None:
        self.vector_store = vector_store
        self.embedder = embedder
        self.llm_model = llm_model
        self.memory = Memory()
        self.agents: Dict[str, Any] = {}

        # Gemini configuration
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(model_name=self.llm_model)

        # Langfuse Observability (fails gracefully if keys are missing)
        self.langfuse = Langfuse()

    def register_agent(self, name: str, agent: Any) -> None:
        self.agents[name] = agent

    def retrieve_context(self, query: str, k: int = 10) -> List[Dict]:
        # CRITICAL: task_type="retrieval_query" for search
        query_embedding = self.embedder.embed_text(query, task_type="retrieval_query")
        return self.vector_store.search(query_embedding, k=k)

    def execute_agent(
        self, agent_name: str, query: str, context: List[Dict], trace: Any
    ) -> Dict:
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not registered")

        # Open a Langfuse span to track this specific agent's latency and token usage
        span = trace.span(
            name=f"agent-{agent_name}",
            input={"query": query, "context_chunks": len(context)},
        )
        
        result = self.agents[agent_name].execute(query, context, self.model)
        
        # Close the span with the output metrics
        span.end(
            output={"analysis_length": len(result.get("analysis", ""))},
            metadata={"sources_used": result.get("sources_used", 0)},
        )
        self.memory.add_agent_result(agent_name, result)
        return result

    def orchestrate(self, query: str, retrieval_k: int = 15) -> Dict:
        self.memory.add_query(query)
        self.memory.add_message("user", query)

        # Open a main Langfuse trace for the entire research request
        trace = self.langfuse.trace(
            name="research-orchestration",
            input={"query": query, "retrieval_k": retrieval_k},
        )

        context = self.retrieve_context(query, k=retrieval_k)

        results: Dict = {}
        for agent_name in self.agents:
            try:
                results[agent_name] = self.execute_agent(
                    agent_name, query, context, trace
                )
            except Exception as e:
                print(f"Error in {agent_name}: {e}")
                results[agent_name] = {"agent": agent_name, "error": str(e), "analysis": ""}

        final_report = self._compile_report(query, results, context)

        trace.update(output={
            "sections": list(results.keys()),
            "num_sources": final_report["num_sources"],
        })
        
        # CRITICAL: Flush traces to the cloud before returning the HTTP response
        self.langfuse.flush()   

        self.memory.add_message("assistant", "report compiled")
        return final_report

    def _compile_report(self, query: str, agent_results: Dict, context: List[Dict]) -> Dict:
        return {
            "query": query,
            "literature_review":  agent_results.get("literature", {}),
            "methods_analysis":   agent_results.get("methods", {}),
            "results_analysis":   agent_results.get("results", {}),
            "critique":           agent_results.get("critique", {}),
            "synthesis":          agent_results.get("synthesis", {}),
            "sources":            self._extract_sources(context),
            "num_sources": len({c.get("paper_id") for c in context if c.get("paper_id")}),
        }

    def _extract_sources(self, context: List[Dict]) -> List[Dict]:
        seen: set = set()
        sources = []
        for chunk in context:
            pid = chunk.get("paper_id")
            if pid and pid not in seen:
                seen.add(pid)
                sources.append({
                    "paper_id":  pid,
                    "title":     chunk.get("title"),
                    "authors":   chunk.get("authors"),
                    "published": chunk.get("published"),
                })
        return sources