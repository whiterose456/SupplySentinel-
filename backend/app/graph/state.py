# backend/app/graph/state.py
from typing import TypedDict, List, Optional, Any

class CrisisState(TypedDict):
    """Shared state for multi-agent negotiation"""
    
    # Scenario data
    scenario_id: str
    scenario_description: str
    
    # Constraints (visible to all agents)
    constraints: dict
    
    # RESTRICTED VIEWS (key innovation!)
    logistics_view: dict      # Only Logistics Chief sees this
    cfo_view: dict            # Only CFO sees this  
    operations_view: dict     # Mediator sees partial view
    
    # Debate state
    debate_log: List[dict]    # [{agent, message, round, timestamp}]
    current_round: int
    max_rounds: int           # Usually 3
    converged: bool
    
    # Final output
    final_plan: Optional[dict]  # {shipping_mode, cost, time, rationale}
    
    # Error handling
    error: Optional[str]