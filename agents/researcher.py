"""
Multi-agent Researcher logic based on LangGraph.
Proves complex loop and state machine handling.
"""

from typing import TypedDict, Annotated, List, Union
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    """The state of our researcher graph."""
    query: str
    research_notes: List[str]
    is_verified: bool
    final_report: str

def researcher_node(state: AgentState):
    """Performs research based on the query."""
    print(f"Researcher: Researching {state['query']}...")
    # Logic to fetch data from tools (e.g. search, docs)
    state["research_notes"].append("Found relevant data about the topic.")
    return state

def verifier_node(state: AgentState):
    """Verifies the research for accuracy and hallucination."""
    print("Verifier: Checking for hallucinations...")
    # Logic to cross-reference notes with grounding docs
    state["is_verified"] = True
    state["final_report"] = "Verified Report: " + " ".join(state["research_notes"])
    return state

def should_continue(state: AgentState):
    """Decision logic for loops."""
    if state["is_verified"]:
        return END
    return "researcher"

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("verifier", verifier_node)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "verifier")
workflow.add_conditional_edges("verifier", should_continue)

app = workflow.compile()

if __name__ == "__main__":
    # Example execution
    inputs = {"query": "Latest trends in low-latency voice AI", "research_notes": [], "is_verified": False, "final_report": ""}
    # for output in app.stream(inputs):
    #     print(output)
    print("LangGraph workflow initialized successfully.")
