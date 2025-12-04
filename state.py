from langgraph.graph import StateGraph,START,END 
from typing import TypedDict, List, Optional

from node import triageAgent, criticAgent, expertAgent, prommptSmith
class AgentState(TypedDict):
    user_query: str
    intent: str                 # Populated by Triage (e.g., "coding", "writing")
    critique: Optional[str]     # Populated by The Critic
    expert_suggestions: List[str] # Populated by The Expert
    final_prompt_draft: str     # Populated by Prompt Smith
    iteration_count: int        # To prevent infinite loops if we add a retry cycle later
    
# Define the state graph for the multi-agent prompt refinement process
graph = StateGraph(AgentState)

graph.add_node("triage", triageAgent)
graph.add_node("critic", criticAgent)
graph.add_node("expert", expertAgent)
graph.add_node("smith", prommptSmith)


graph.add_edge(START, "triage")
graph.add_edge("triage", "critic")
graph.add_edge("critic", "expert")
graph.add_edge("expert", "smith")
graph.add_edge("smith", END)

promptify = graph.compile()