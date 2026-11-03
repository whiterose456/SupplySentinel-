# SupplySentinel

A multi-agent supply chain crisis simulation that explores how AI agents can coordinate decisions when disruptions put logistics, budgets, and service-level commitments under pressure.

SupplySentinel brings together role-based agents, a scenario-driven workflow, and an evaluation layer to make crisis-response decisions easier to inspect and compare.

## Overview

Supply chains involve competing priorities. A logistics team may need to reroute shipments, while finance is concerned about cost and a mediator must help reconcile conflicting recommendations.

This project models that kind of decision-making through a coordinated multi-agent workflow.

### Core capabilities

- **Scenario configuration** — define supply-chain disruption scenarios for simulation.
- **Role-based agent reasoning** — specialized agents consider financial, logistics, and coordination concerns.
- **Negotiation interface** — inspect the discussion and decisions produced during a simulation.
- **Operational dashboard** — review cost impact, service-level status, and risk indicators.
- **Baseline evaluation** — compare multi-agent results with baseline or heuristic approaches using the included evaluation scripts.

> **Project status:** This repository is a hackathon/prototype project. Features and integrations may be incomplete; check the implementation before relying on it in a production environment.

## Agent Roles

The backend uses a LangGraph-based workflow to coordinate three roles:

| Agent | Responsibility |
| --- | --- |
| **CFO Agent** | Considers financial impact, profit margins, and budget constraints. |
| **Logistics Agent** | Considers shipping routes, inventory levels, and carrier constraints. |
| **Mediator Agent** | Helps reconcile conflicting priorities and move the workflow toward a decision. |

The agents represent different operational perspectives rather than independent production systems.

## Architecture

| Layer | Technologies | Purpose |
| --- | --- | --- |
| Backend | Python, FastAPI, LangGraph | API and multi-agent orchestration |
| Frontend | Next.js, React, TypeScript, Tailwind CSS | Scenario and simulation interface |
| Model access | Qwen / DashScope | LLM-powered agent responses |
| Evaluation | Python scripts and pytest | Import checks, baseline runs, and simulation comparisons |

At a high level, a scenario is submitted through the application, the backend coordinates the participating agents, and the resulting decisions can be inspected in the frontend and evaluated against a baseline.

## Repository Structure

The project is organized around three main areas:

- `backend/` — FastAPI application, agent workflow, and evaluation scripts.
- `frontend/` — Next.js user interface.
- `backend/eval/` — scripts for baseline and multi-agent evaluation.

See the source directories for the current implementation details.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Node.js and npm
- A Qwen / DashScope API credential if you want to run model-backed agent workflows

### 1. Clone the repository

```bash
git clone https://github.com/whiterose456/SupplySentinel-.git
cd SupplySentinel-
```

### 2. Set up the backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

**Windows (PowerShell)**

```powershell
.venv\\Scripts\\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install the dependencies and start the API:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API should then be available at `http://localhost:8000` (assuming the default Uvicorn configuration).

### 3. Set up the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000).

### Configuration

The agent workflow requires access to the configured LLM provider. Before running model-backed scenarios, inspect the backend configuration and provide the required DashScope/Qwen credential using the environment variable or configuration mechanism expected by the application.

Do not commit API keys or other secrets to the repository.

## Evaluation

The repository includes scripts intended to compare baseline behavior with multi-agent simulation results.

Run these commands from the repository root unless otherwise noted:

```bash
# Run backend tests
cd backend
pytest
cd ..

# Check backend imports
python backend/test_imports.py

# Record baseline responses
python backend/eval/run_baseline.py

# Run the multi-agent simulation
python backend/eval/run_multiagent.py
```

Use the evaluation scoring script (`score.py`) to inspect comparison metrics. Check the script's location and expected input files in the repository before running it.

## Technology Stack

- **Language:** Python, TypeScript
- **Backend:** FastAPI
- **Agent orchestration:** LangGraph
- **LLM provider:** Qwen / DashScope
- **Frontend:** Next.js, React, Tailwind CSS
- **Testing and evaluation:** pytest and custom Python scripts

## Design Goals

- Make multi-agent decision-making observable rather than treating the model as a black box.
- Represent competing supply-chain priorities through distinct agent roles.
- Provide a repeatable way to run scenarios and compare approaches.
- Keep the system modular so additional agents, constraints, and disruption scenarios can be explored.

## Limitations

This is an experimental simulation, not a live supply-chain control system. Outputs depend on the scenario configuration and model responses. They should not be treated as verified operational, financial, or logistics advice.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
