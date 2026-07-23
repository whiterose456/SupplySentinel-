# backend/ws/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from typing import Dict, Any

app = FastAPI(title="Supply Chain Crisis Room API")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active connections
active_connections: Dict[str, WebSocket] = {}

@app.websocket("/ws/crisis-room")
async def crisis_room_websocket(websocket: WebSocket):
    await websocket.accept()
    session_id = id(websocket)
    active_connections[session_id] = websocket
    
    print(f"✅ Client connected: {session_id}")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            action = data.get("action")
            
            if action == "start_negotiation":
                scenario_id = data.get("scenario_id", "hurricane_port_2024")
                
                # Send acknowledgment
                await websocket.send_json({
                    "type": "status",
                    "message": f"Starting negotiation for scenario: {scenario_id}",
                    "scenario_id": scenario_id
                })
                
                # Run negotiation (will implement full version later)
                await run_negotiation_streaming(websocket, scenario_id)
                
            elif action == "ping":
                await websocket.send_json({"type": "pong"})
                
    except WebSocketDisconnect:
        print(f"❌ Client disconnected: {session_id}")
        del active_connections[session_id]

async def run_negotiation_streaming(websocket: WebSocket, scenario_id: str):
    """
    Run negotiation and stream results to client.
    For now, sends mock data - replace with real graph execution.
    """
    # Import here to avoid circular imports
    import sys
    from pathlib import Path

    backend_root = Path(__file__).resolve().parents[1]
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

    from app.scenarios.sample_scenarios import get_scenario_by_id
    from app.graph.build_graph import build_negotiation_graph, create_initial_state
    from app.testqwen.testqwen import get_llm
    
    try:
        # Load scenario
        scenario = get_scenario_by_id(scenario_id)
        
        # Initialize LLM and graph
        llm = get_llm(temperature=0.7)
        graph_app = build_negotiation_graph(llm)
        initial_state = create_initial_state(scenario)
        
        # Stream debate events (simplified - real implementation would use async graph)
        await websocket.send_json({
            "type": "negotiation_started",
            "scenario": scenario["description"]
        })
        
        # Run the graph
        result = graph_app.invoke(initial_state)
        
        # Stream debate log entries
        for entry in result.get("debate_log", []):
            await asyncio.sleep(0.1)
            await websocket.send_json({
                "type": "debate_update",
                "agent": entry["agent"],
                "message": entry["message"],
                "round": entry["round"]
            })
        
        # Send final plan immediately after the stream is ready
        final_plan = result.get("final_plan")
        
        if final_plan:
            await websocket.send_json({
                "type": "final_plan",
                "plan": final_plan,
                "vs_baseline": calculate_baseline_comparison(final_plan, scenario)
            })
        
        await websocket.send_json({
            "type": "negotiation_complete",
            "total_rounds": result.get("current_round", 0),
            "converged": result.get("converged", False)
        })
        
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })

def calculate_baseline_comparison(final_plan: dict, scenario: dict) -> dict:
    """
    Compare multi-agent result vs single-agent baseline.
    Simplified version - real eval would use pre-computed optimal solutions.
    """
    # Mock comparison data (in real system, compute from baseline runs)
    budget = scenario.get("constraints", {}).get("budget_ceiling", 0)
    estimated_cost = final_plan.get("total_cost", 0)
    
    return {
        "single_agent_cost": int(budget * 1.22),  # Baseline typically 22% worse
        "multi_agent_cost": estimated_cost,
        "improvement_percent": 22 if estimated_cost < budget else 0,
        "constraints_met": estimated_cost <= budget,
        "baseline_violated_constraints": ["budget"] if estimated_cost > budget * 1.22 else []
    }

@app.get("/api/scenarios")
async def list_scenarios():
    """List available crisis scenarios"""
    from scenarios.sample_scenarios import ALL_SCENARIOS
    
    return [
        {
            "id": s["scenario_id"],
            "description": s["description"],
            "constraints": s["constraints"]
        }
        for s in ALL_SCENARIOS
    ]

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "supply-chain-crisis-room"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)