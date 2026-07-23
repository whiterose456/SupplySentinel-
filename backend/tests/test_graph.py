import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.graph.build_graph import graph
from app.graph.nodes import propose_plan, critique_plan, finalize_plan
from app.agents.mediator_agent import mediator_node


def test_graph_compiles_and_runs():
    state = {
        "scenario": "Port disruption",
        "constraints": {
            "total_units": 5000,
            "deadline_days": 7,
            "budget_usd": 250000,
            "penalty_per_day_late": 1500,
        },
        "logistics_view": {
            "air_freight_cost_per_unit": 12,
            "air_freight_days": 2,
            "sea_freight_cost_per_unit": 4,
            "sea_freight_days": 10,
            "carrier_reliability_air": 0.95,
            "carrier_reliability_sea": 0.8,
        },
        "cfo_view": {
            "budget_usd": 250000,
            "cost_overrun_tolerance_pct": 0.1,
        },
        "debate_log": [],
        "round": 0,
        "converged": False,
        "final_plan": None,
    }

    result = graph.invoke(state)
    assert result["converged"] is True
    assert result["final_plan"] is not None
    assert result["final_plan"]["rationale"]


def test_node_helpers_update_state():
    state = {
        "messages": [],
        "debate_log": [],
        "round": 0,
    }

    proposal = propose_plan(state)
    critique = critique_plan(proposal)
    final = finalize_plan(critique)

    assert proposal["messages"]
    assert critique["messages"]
    assert final["final_plan"]["rationale"]


def test_mediator_extracts_structured_plan_from_text_response():
    class DummyResponse:
        def __init__(self, content):
            self.content = content

    class DummyLLM:
        def __init__(self, content):
            self.content = content

        def invoke(self, messages):
            return DummyResponse(self.content)

    state = {
        "debate_log": [],
        "current_round": 3,
        "max_rounds": 3,
        "operations_view": {},
        "constraints": {},
    }

    response_text = (
        'FORCED COMPROMISE RULING — EXECUTION PLAN '
        '{shipping_mode: "Hybrid: 8,000 units by standard truck + 2,000 units by air", '
        'total_cost: 29600, delivery_time: 3, rationale: "This is the only option that meets the constraints."}'
    )

    result = mediator_node(state, DummyLLM(response_text))

    assert result["final_plan"]["shipping_mode"] == "Hybrid: 8,000 units by standard truck + 2,000 units by air"
    assert result["final_plan"]["total_cost"] == 29600
    assert result["final_plan"]["delivery_time"] == 3
    assert result["final_plan"]["forced"] is True
