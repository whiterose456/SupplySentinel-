# backend/app/graph/edges.py
from .state import CrisisState


def route_after_cfo(state: CrisisState) -> str:
    """Determine where to go after CFO speaks."""
    current_round = state.get("current_round", state.get("round", 1))
    max_rounds = state.get("max_rounds", 3)

    if current_round >= max_rounds:
        return "mediator"

    return "round_handler"


def increment_round(state: CrisisState) -> dict:
    """Increment round counter between cycles."""
    current_round = state.get("current_round")
    if current_round is None:
        current_round = state.get("round", 1)
    if current_round is None:
        current_round = 1
    next_round = int(current_round) + 1
    return {
        "current_round": next_round,
        "round": next_round,
    }
