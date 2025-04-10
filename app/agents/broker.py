from datetime import datetime
from typing import Dict, List


# ---------- In-Memory Registry ----------
class AgentRegistry:
    def __init__(self) -> None:
        self.agents: Dict[str, Dict] = {}

    def register(self, agent_data: Dict) -> None:
        name = agent_data["name"]
        if name in self.agents:
            raise ValueError(f"Agent '{name}' already exists.")

        self.agents[name] = {
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
