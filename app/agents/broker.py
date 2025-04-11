from datetime import datetime
from typing import Dict, List


class AgentBroker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.agents: Dict[str, Dict] = {}
        return cls._instance

    def register(self, agent_data: Dict) -> None:
        """In-memory registry for agents."""
        name = agent_data["name"]
        if name in self.agents:
            raise ValueError(f"Agent '{name}' already exists.")

        self.agents[name] = {
            "name": name,
            "endpoint": agent_data["endpoint"],
            "description": agent_data["description"],
            "skills": agent_data["skills"],
            "type": agent_data.get("type", "llm"),
            "registered_at": datetime.now().isoformat(),
        }

    def get_agent(self, name: str) -> Dict:
        if name not in self.agents:
            raise ValueError(f"Agent '{name}' not found.")
        return self.agents[name]

    def list_agents(self) -> List[Dict]:
        return list(self.agents.values())
