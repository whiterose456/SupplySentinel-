def logistics_agent_prompt() -> str:
    return """You are the Logistics Chief in a supply chain crisis negotiation room.

YOUR PRIORITY: Speed and delivery reliability
WHAT YOU SEE: Carrier capacities, transit times, reliability scores
WHAT YOU DON'T SEE: Exact costs (that's the CFO's domain)

YOUR ROLE IN DEBATE:
1. Advocate for fastest, most reliable shipping options
2. Push back on cheap-but-slow proposals from CFO
3. You CAN disclose: transit times, capacity limits, reliability risks during debate
4. You CANNOT see: budget constraints directly

NEGOTIATION RULES:
- Respond to CFO's proposals with logistics feasibility analysis
- If proposal is too slow or unreliable, explain risks and suggest faster options
- After 3 rounds without agreement, accept Mediator's ruling
- Keep responses concise (2-3 sentences max)

RESPOND with your logistics assessment and counter-proposal if needed."""

def build_logistics_context(state: dict) -> str:
    """Build Logistics Chief's restricted view"""
    logistics_view = state.get("logistics_view", {})
    constraints = state.get("constraints", {})
    
    return f"""LOGISTICS DATA (Your Domain):
- Carrier capacities: {logistics_view.get('carrier_capacity', {})}
- Transit times (days): {logistics_view.get('transit_times', {})}
- Reliability rates: {logistics_view.get('reliability', {})}
- Hidden info (reveal strategically): {logistics_view.get('hidden_info', 'None')}

SCENARIO REQUIREMENTS:
- Units needed: {constraints.get('units_needed', 'N/A')}
- Deadline: {constraints.get('deadline_days', 'N/A')} days
- Min reliability required: {constraints.get('min_reliability', 'N/A')}"""

def logistics_chief_node(state: dict, llm) -> dict:
    """Logistics Chief agent node function"""
    from langchain_core.messages import SystemMessage, HumanMessage
    
    context = build_logistics_context(state)
    
    # Get last few messages from CFO for context
    recent_debate = [entry for entry in state.get("debate_log", []) 
                     if entry["agent"] == "cfo"][-2:]
    debate_history = "\n".join([f"- {m['message']}" for m in recent_debate]) if recent_debate else "[No previous proposals - you go first]"
    
    messages = [
        SystemMessage(content=logistics_agent_prompt()),
        HumanMessage(content=f"""{context}

CFO's recent position(s):
{debate_history}

Current round: {state.get('current_round', 1)} / {state.get('max_rounds', 3)}

Provide your logistics recommendation and reasoning.""")
    ]
    
    response = llm.invoke(messages)
    
    return {
        "debate_log": state.get("debate_log", []) + [{
            "agent": "logistics_chief",
            "message": response.content,
            "round": state.get("current_round", 1)
        }]
    }