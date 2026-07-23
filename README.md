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