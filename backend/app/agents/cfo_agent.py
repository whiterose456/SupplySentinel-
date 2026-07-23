def cfo_agent_prompt() -> str:
    return """You are the CFO (Chief Financial Officer) in a supply chain crisis negotiation room.

YOUR PRIORITY: Cost minimization and budget compliance
WHAT YOU SEE: Cost per shipping mode, budget constraints, financial flexibility
WHAT YOU DON'T SEE: Exact carrier capacities or reliability scores (that's Logistics)

YOUR ROLE IN DEBATE:
1. Advocate for cheapest viable shipping options
2. Push back on expensive proposals from Logistics Chief
3. You CAN disclose: cost data, budget limits during debate
4. You CANNOT see: carrier capacity limits directly

NEGOTIATION RULES:
- Respond to Logistics Chief's proposals with cost analysis
- If proposal exceeds budget, explain by how much and suggest alternatives
- After 3 rounds without agreement, accept Mediator's ruling
- Keep responses concise (2-3 sentences max)

RESPOND with your cost assessment and counter-proposal if needed."""

def build_cfo_context(state: dict) -> str:
    """Build CFO's restricted view of scenario"""
    cfo_view = state.get("cfo_view", {})
    constraints = state.get("constraints", {})
    
    return f"""FINANCIAL DATA (Your Domain):
- Cost per unit by mode: {cfo_view.get('cost_per_unit', {})}
- Budget ceiling: ${constraints.get('budget_ceiling', 'N/A')}
- Budget flexibility: {cfo_view.get('budget_flexibility', 'None')}
- Hidden info (reveal strategically): {cfo_view.get('hidden_info', 'None')}

SCENARIO CONSTRAINTS:
- Units needed: {constraints.get('units_needed', 'N/A')}
- Deadline: {constraints.get('deadline_days', 'N/A')} days"""

def cfo_node(state: dict, llm) -> dict:
    """CFO agent node function"""
    from langchain_core.messages import SystemMessage, HumanMessage
    
    context = build_cfo_context(state)
    
    # Get last few messages from Logistics Chief for context
    recent_debate = [entry for entry in state.get("debate_log", []) 
                     if entry["agent"] == "logistics_chief"][-2:]
    debate_history = "\n".join([f"- {m['message']}" for m in recent_debate]) if recent_debate else "[No previous proposals]"
    
    messages = [
        SystemMessage(content=cfo_agent_prompt()),
        HumanMessage(content=f"""{context}

Logistics Chief's recent proposal(s):
{debate_history}

Current round: {state.get('current_round', 1)} / {state.get('max_rounds', 3)}

Provide your cost assessment and counter-proposal.""")
    ]
    
    response = llm.invoke(messages)
    
    return {
        "debate_log": state.get("debate_log", []) + [{
            "agent": "cfo",
            "message": response.content,
            "round": state.get("current_round", 1)
        }]
    }