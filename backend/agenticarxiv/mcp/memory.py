from typing import List, Dict, Optional
from datetime import datetime

class Memory:
    """Stores conversation history and agent interactions for MCP controller."""
    
    def __init__(self):
        self.messages = []
        self.agent_results = {}
        self.query_history = []
    
    def add_message(self, role: str, content: str):
        self.messages.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_agent_result(self, agent_name: str, result: Dict):
        if agent_name not in self.agent_results:
            self.agent_results[agent_name] = []
        
        self.agent_results[agent_name].append({
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_query(self, query: str, context: Optional[Dict] = None):
        self.query_history.append({
            'query': query,
            'context': context or {},
            'timestamp': datetime.now().isoformat()
        })
    
    def get_messages(self, limit: Optional[int] = None) -> List[Dict]:
        if limit:
            return self.messages[-limit:]
        return self.messages
    
    def get_agent_result(self, agent_name: str) -> Optional[Dict]:
        if agent_name in self.agent_results and self.agent_results[agent_name]:
            return self.agent_results[agent_name][-1]['result']
        return None
    
    def get_all_agent_results(self) -> Dict:
        return {
            agent: results[-1]['result'] if results else None
            for agent, results in self.agent_results.items()
        }
    
    def clear(self):
        self.messages = []
        self.agent_results = {}
        self.query_history = []