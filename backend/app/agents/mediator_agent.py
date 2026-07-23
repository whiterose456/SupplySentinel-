def mediator_agent_prompt() -> str:
    return """You are the Operations Director / PR Director - the MEDIATOR in this crisis negotiation.

YOUR PRIORITY: Balanced solution that satisfies hard constraints
WHAT YOU SEE: Partial view of both sides + hard constraints that CANNOT be violated
YOUR POWER: Forced compromise ruling if no agreement after 3 rounds

MEDIATION APPROACH:
1. Review debate transcript - what did each side reveal?
2. Identify non-negotiable hard constraints (e.g., "must deliver in 7 days")
3. Weigh disclosed trade-offs (Logistics wants speed, CFO wants low cost)
4. Issue FINAL PLAN that:
   - Meets ALL hard constraints (budget, deadline, reliability)
   - Balances competing priorities fairly
   - Uses ONLY information disclosed during debate (no cheating!)

FORCED RULING PROTOCOL (if invoked after round 3):
- You only know what was said in debate_log
- Must produce executable plan: {{shipping_mode, total_cost, delivery_time, rationale}}
- Explain why you ruled this way based on disclosed information

RESPOND with your mediation assessment or final ruling."""

def build_mediator_context(state: dict) -> str:
    """Build Mediator's partial view."""
    ops_view = state.get("operations_view") or {}
    debate_log = state.get("debate_log", []) or []
    constraints = state.get("constraints", {}) or {}

    debate_text = "\n".join([
        f"Round {entry.get('round', 0)} - {str(entry.get('agent', 'agent')).upper()}: {entry.get('message', '')}"
        for entry in debate_log[-8:]
    ]) if debate_log else "[No debate yet]"

    current_round = state.get("current_round")
    if current_round is None:
        current_round = state.get("round", 0)
    if current_round is None:
        current_round = 0
    max_rounds = state.get("max_rounds")
    if max_rounds is None:
        max_rounds = 3

    return f"""VISIBLE CONSTRAINTS (Non-negotiable):
{ops_view.get('visible_constraints', [])}

HARD CONSTRAINTS (Cannot violate under any circumstance):
{ops_view.get('hard_constraints', [])}

FULL DEBATE TRANSCRIPT (What has been revealed):
{debate_text}

MEDIATOR-ONLY INTELLIGENCE (Not known to other agents):
{ops_view.get('mediator_only_data', 'None')}

CURRENT ROUND: {current_round} / {max_rounds}
STATUS: {'FORCED RULING REQUIRED' if current_round >= max_rounds else 'Assessing convergence'}"""

def _parse_final_plan(response_text: str, is_forced: bool) -> dict:
    """Extract a structured final plan from the mediator's response text."""
    import re

    plan = {
        "shipping_mode": "truck",
        "total_cost": 0,
        "delivery_time": 0,
        "rationale": response_text,
        "forced": is_forced,
        "mediator_statement": response_text,
    }

    match = re.search(r"\{([^{}]+)\}", response_text)
    if not match:
        return plan

    payload = match.group(1)
    shipping_mode_match = re.search(r"shipping_mode:\s*\"([^\"]+)\"", payload)
    if shipping_mode_match:
        plan["shipping_mode"] = shipping_mode_match.group(1)

    cost_match = re.search(r"total_cost:\s*(\d+)", payload)
    if cost_match:
        plan["total_cost"] = int(cost_match.group(1))

    time_match = re.search(r"delivery_time:\s*(\d+)", payload)
    if time_match:
        plan["delivery_time"] = int(time_match.group(1))

    rationale_match = re.search(r"rationale:\s*\"([^\"]+)\"", payload)
    if rationale_match:
        plan["rationale"] = rationale_match.group(1)

    return plan


def mediator_node(state: dict, llm) -> dict:
    """Mediator node - issues compromise ruling."""
    from langchain_core.messages import SystemMessage, HumanMessage

    context = build_mediator_context(state)

    current_round = state.get("current_round")
    if current_round is None:
        current_round = state.get("round", 0)
    max_rounds = state.get("max_rounds")
    if max_rounds is None:
        max_rounds = 3
    is_forced = current_round >= max_rounds

    messages = [
        SystemMessage(content=mediator_agent_prompt()),
        HumanMessage(content=f"""{context}

{'ISSUE YOUR FORCED COMPROMISE RULING NOW' if is_forced else 'Assess whether convergence has been achieved'}

{'Provide the FINAL EXECUTION PLAN with specific mode, cost, and time.' if is_forced else 'If not converged, explain what needs to be resolved.'}""")
    ]

    response = llm.invoke(messages)
    response_text = response.content if hasattr(response, "content") else str(response)
    final_plan = _parse_final_plan(response_text, is_forced)

    return {
        "final_plan": final_plan,
        "converged": True,
        "debate_log": state.get("debate_log", []) + [{
            "agent": "mediator",
            "message": response_text,
            "round": state.get("current_round", 1)
        }]
    }