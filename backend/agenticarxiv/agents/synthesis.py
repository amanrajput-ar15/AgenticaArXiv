import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from typing import List, Dict

class SynthesisAgent:
    """Synthesizes insights from all analyses to identify research gaps and opportunities."""
    
    SYSTEM_PROMPT = """You are a research synthesizer. Your task is to:
1. Integrate insights from literature, methods, results, and critiques
2. Identify research gaps and unexplored areas
3. Suggest promising research directions
4. Provide a cohesive synthesis of the field

Think holistically about the research landscape."""
    
    def execute(self, query: str, context: List[Dict], *args, **kwargs) -> Dict:
        """Execute synthesis analysis."""
        context_text = self._format_context(context)
        
        user_message = f"""Research Question: {query}

Relevant Papers:
{context_text}

Provide a comprehensive synthesis covering:
1. Integration of key findings across papers
2. Identification of research gaps
3. Promising future research directions
4. Novel opportunities for contribution"""
        
        agent_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=self.SYSTEM_PROMPT
        )
        
        response = agent_model.generate_content(
            user_message,
            generation_config=GenerationConfig(temperature=0.4) # Highest temperature for synthesis
        )
        
        return {
            'agent': 'synthesis',
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
                )
            
            formatted.append(f"Content: {chunk.get('text', '')[:600]}\n")
        
        return '\n---\n'.join(formatted[:12])