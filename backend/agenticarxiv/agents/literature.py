import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from typing import List, Dict

class LiteratureAgent:
    """Analyzes related work and literature in research papers."""
    
    SYSTEM_PROMPT = """You are a research literature analyst. Your task is to:
1. Identify key papers and prior work related to the query
2. Summarize the main contributions of each relevant paper
3. Identify trends and evolution in the field
4. Highlight seminal works and influential papers

Provide structured output with clear citations."""
    
    def execute(self, query: str, context: List[Dict], *args, **kwargs) -> Dict:
        """
        Execute literature analysis.
        *args and **kwargs are used to safely ignore legacy 'client' and 'model' params 
        passed by the old controller until we refactor it.
        """
        context_text = self._format_context(context)
        
        user_message = f"""Research Question: {query}

Relevant Papers:
{context_text}

Provide a comprehensive literature review covering:
1. Key related works
2. Main contributions from each paper
3. Trends and evolution in the field
4. Gaps in existing literature"""
        
        # Instantiate the model with its strict persona
        agent_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=self.SYSTEM_PROMPT
        )
        
        response = agent_model.generate_content(
            user_message,
            generation_config=GenerationConfig(temperature=0.3)
        )
        
        return {
            'agent': 'literature',
            'analysis': response.text,
            'sources_used': len(set([c.get('paper_id') for c in context if c.get('paper_id')]))
        }
    
    def _format_context(self, context: List[Dict]) -> str:
        """Format context chunks for prompt."""
        formatted = []
        seen_papers = set()
        
        for chunk in context:
            paper_id = chunk.get('paper_id')
            if paper_id and paper_id not in seen_papers:
                seen_papers.add(paper_id)
                formatted.append(
                    f"Paper: {chunk.get('title')}\n"
                    f"Authors: {', '.join(chunk.get('authors', []))}\n"
                    f"Published: {chunk.get('published')}\n"
                )
            
            formatted.append(f"Content: {chunk.get('text', '')[:800]}\n")
        
        return '\n---\n'.join(formatted[:10])