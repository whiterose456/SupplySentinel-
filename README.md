# Supply Chain Crisis Room

A hackathon project for simulating multi-agent supply chain crisis negotiations.

## Structure

- Backend: FastAPI + LangGraph + Qwen/Dashscope
- Frontend: Next.js + React + TypeScript
- Evaluation: scenario scoring and comparison scripts

## Project Vision

**Cyclops Logistic** is a state-of-the-art simulation platform designed to model, analyze, and optimize supply chain operations during high-stakes crises. By utilizing advanced multi-agent systems, it enables real-time negotiation, decision-making, and risk management.

## Getting Started

### Backend Setup
1. Navigate to `backend` directory
2. Create a virtual environment: `python -m venv .venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the FastAPI server: `uvicorn app.main:app --reload`

### Frontend Setup
1. Navigate to `frontend` directory
2. Install Node packages: `npm install`
3. Start the Next.js development server: `npm run dev`
4. Open `http://localhost:3000` in your browser

## Multi-Agent Architecture

The backend employs a LangGraph workflow orchestrating three key agents:
- **CFO Agent**: Evaluates financial impacts, profit margins, and budget constraints.
- **Logistics Agent**: Manages shipping routes, inventory levels, and carrier contracts.
- **Mediator Agent**: Facilitates consensus and resolves conflicts between departments.

## Key Features

- **Interactive Scenario Builder**: Configure crisis situations dynamically.
- **Live Negotiation Chat**: Watch agents debate and align on options.
- **Real-Time Financial Dashboard**: Track cost impact, SLA status, and risk index live.

## Evaluation & Baseline Testing

We provide scripts to score simulation outcomes and compare multi-agent negotiations against baseline heuristics:
- Run `python backend/eval/run_baseline.py` to record baseline responses.
- Run `python backend/eval/run_multiagent.py` to run the agent-based simulation.
- Use `score.py` to print comparison metrics.

## Technology Stack

- **Backend**: Python, FastAPI, LangGraph, Qwen/Dashscope API
- **Frontend**: React, Next.js, Tailwind CSS, TypeScript, WebSockets
- **Simulation Engine**: Custom state machine with prompt-guided LLM agents

## License

This project is licensed under the MIT License - see the LICENSE file for details.