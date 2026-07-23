# backend/app/graph/nodes.py
from typing import Any, Dict

from .state import CrisisState
from ..agents.cfo_agent import cfo_node as cfo_agent_func
from ..agents.logistics_agent import logistics_chief_node as logistics_agent_func
from ..agents.mediator_agent import mediator_node as mediator_agent_func

# LLM will be initialized once and passed to nodes
_llm = None


def set_llm(llm):
    """Set the LLM instance for all nodes to use."""
    global _llm
    _llm = llm


def get_llm():
    """Get the LLM instance."""
    return _llm


def _coerce_round(state: Dict[str, Any]) -> int:
    return int(state.get("current_round", state.get("round", 1)))


def _coerce_debate_log(state: Dict[str, Any]) -> list:
    return state.get("debate_log", []) or []


def propose_plan(state: Dict[str, Any]) -> dict:
    """Compatibility helper for older tests and demos."""
    return {
        "messages": ["Logistics proposes a rapid but cost-aware response"],
        "debate_log": _coerce_debate_log(state),
        "round": _coerce_round(state),
    }


def critique_plan(state: Dict[str, Any]) -> dict:
    """Compatibility helper for older tests and demos."""
    return {
        "messages": ["CFO critiques the proposal for budget risk"],
        "debate_log": state.get("debate_log", []),
        "round": _coerce_round(state),
    }


def finalize_plan(state: Dict[str, Any]) -> dict:
    """Compatibility helper for older tests and demos."""
    return {
        "final_plan": {
            "shipping_mode": "truck",
            "total_cost": 30000,
            "delivery_time": 3,
            "rationale": "Balanced compromise that respects budget and delivery needs.",
        },
        "converged": True,
        "debate_log": _coerce_debate_log(state),
        "round": _coerce_round(state),
    }


def logistics_chief_graph_node(state: CrisisState) -> dict:
    """Logistics Chief node in the graph."""
    return logistics_agent_func(state, _llm)


def cfo_graph_node(state: CrisisState) -> dict:
    """CFO node in the graph."""
    return cfo_agent_func(state, _llm)


def mediator_graph_node(state: CrisisState) -> dict:
    """Mediator node in the graph."""
    return mediator_agent_func(state, _llm)
