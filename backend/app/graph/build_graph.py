# backend/app/graph/build_graph.py
from langgraph.graph import StateGraph, END

from .state import CrisisState
from .nodes import logistics_chief_graph_node, cfo_graph_node, mediator_graph_node, set_llm
from .edges import route_after_cfo, increment_round


def build_negotiation_graph(llm=None):
    """Build the multi-agent negotiation graph."""
    if llm is None:
        from ..testqwen.testqwen import get_llm as get_test_llm

        llm = get_test_llm()

    # Set LLM instance for all nodes
    set_llm(llm)

    workflow = StateGraph(CrisisState)

    # Add nodes
    workflow.add_node("logistics", logistics_chief_graph_node)
    workflow.add_node("cfo", cfo_graph_node)
    workflow.add_node("round_handler", increment_round)
    workflow.add_node("mediator", mediator_graph_node)

    # Define edges
    workflow.add_edge("logistics", "cfo")

    workflow.add_conditional_edges(
        "cfo",
        route_after_cfo,
        {
            "round_handler": "round_handler",
            "mediator": "mediator",
        },
    )

    workflow.add_edge("round_handler", "logistics")
    workflow.add_edge("mediator", END)

    workflow.set_entry_point("logistics")
    app = workflow.compile()
    return app


def create_initial_state(scenario: dict) -> CrisisState:
    """Initialize state from scenario definition."""
    return {
        "scenario_id": scenario.get("scenario_id", "unknown"),
        "scenario_description": scenario.get("description", ""),
        "constraints": scenario.get("constraints", {}),
        "logistics_view": scenario.get("logistics_view", {}),
        "cfo_view": scenario.get("cfo_view", {}),
        "operations_view": scenario.get("operations_view", {}),
        "debate_log": [],
        "current_round": 1,
        "round": 1,
        "max_rounds": scenario.get("max_rounds", 3),
        "converged": False,
        "final_plan": None,
        "error": None,
    }


graph = build_negotiation_graph(None)
