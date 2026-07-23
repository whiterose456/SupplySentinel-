import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MODULES = [
    ("backend.app.graph.state", "CrisisState"),
    ("backend.app.agents.cfo_agent", "cfo_agent_prompt"),
    ("backend.app.agents.logistics_agent", "logistics_agent_prompt"),
    ("backend.app.agents.mediator_agent", "mediator_agent_prompt"),
    ("backend.app.graph.nodes", "logistics_chief_graph_node"),
    ("backend.app.graph.edges", "route_after_cfo"),
    ("backend.app.graph.build_graph", "build_negotiation_graph"),
    ("backend.app.scenarios.sample_scenarios", "HURRICANE_PORT_CLOSURE"),
    ("backend.app.testqwen.testqwen", "get_llm"),
    ("backend.app.main", "app"),
]

for module_name, symbol in MODULES:
    module = importlib.import_module(module_name)
    attr = getattr(module, symbol)
    print(f"OK: {module_name} -> {symbol}")

print("All import checks passed")
