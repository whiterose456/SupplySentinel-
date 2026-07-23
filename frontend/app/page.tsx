// frontend/app/page.tsx
'use client';

import { useState, useEffect, useRef } from 'react';

interface DebateEntry {
  agent: string;
  message: string;
  round: number;
}

interface FinalPlan {
  shipping_mode: string;
  total_cost: number;
  delivery_time: number;
  rationale: string;
  forced: boolean;
}

interface BaselineComparison {
  single_agent_cost: number;
  multi_agent_cost: number;
  improvement_percent: number;
  constraints_met: boolean;
}

export default function CrisisRoom() {
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [debateLog, setDebateLog] = useState<DebateEntry[]>([]);
  const [finalPlan, setFinalPlan] = useState<FinalPlan | null>(null);
  const [baseline, setBaseline] = useState<BaselineComparison | null>(null);
  const [status, setStatus] = useState<string>('Ready to start');
  const [selectedScenario, setSelectedScenario] = useState('hurricane_port_2024');
  const [isRunning, setIsRunning] = useState(false);

  const debateEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    debateEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [debateLog]);

  useEffect(() => {
    const websocket = new WebSocket('ws://127.0.0.1:8000/ws/crisis-room');

    websocket.onopen = () => {
      setConnected(true);
      setWs(websocket);
      setStatus('Connected and ready for negotiation');
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      switch (data.type) {
        case 'status':
          setStatus(data.message);
          break;
        case 'debate_update':
          setDebateLog((prev) => [
            ...prev,
            {
              agent: data.agent,
              message: data.message,
              round: data.round,
            },
          ]);
          break;
        case 'final_plan':
          setFinalPlan(data.plan);
          setBaseline(data.vs_baseline);
          setIsRunning(false);
          setStatus('Negotiation complete');
          break;
        case 'negotiation_complete':
          setIsRunning(false);
          setStatus(`Complete in ${data.total_rounds} rounds`);
          break;
        case 'error':
          setStatus(`Error: ${data.message}`);
          setIsRunning(false);
          break;
      }
    };

    websocket.onclose = () => {
      setConnected(false);
      setWs(null);
      setStatus('Connection lost - retrying is available');
    };

    return () => {
      websocket.close();
    };
  }, []);

  const startNegotiation = () => {
    if (!ws || !connected) return;

    setDebateLog([]);
    setFinalPlan(null);
    setBaseline(null);
    setIsRunning(true);
    setStatus('Starting negotiation...');

    ws.send(
      JSON.stringify({
        action: 'start_negotiation',
        scenario_id: selectedScenario,
      })
    );
  };

  const getAgentColor = (agent: string) => {
    switch (agent) {
      case 'logistics_chief':
        return 'border-cyan-400/70 bg-cyan-500/10 text-cyan-50';
      case 'cfo':
        return 'border-emerald-400/70 bg-emerald-500/10 text-emerald-50';
      case 'mediator':
        return 'border-violet-400/70 bg-violet-500/10 text-violet-50';
      default:
        return 'border-slate-500/70 bg-slate-500/10 text-slate-50';
    }
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(34,211,238,0.12),_transparent_28%),radial-gradient(circle_at_top_right,_rgba(168,85,247,0.16),_transparent_30%),linear-gradient(135deg,_#020617_0%,_#0f172a_55%,_#111827_100%)] text-slate-100 p-4 sm:p-6 lg:p-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-6">
        <header className="overflow-hidden rounded-[28px] border border-slate-800/70 bg-slate-950/70 shadow-[0_24px_80px_rgba(0,0,0,0.35)] backdrop-blur-xl">
          <div className="flex flex-col gap-8 px-6 py-8 sm:px-8 lg:flex-row lg:items-end lg:justify-between lg:px-10">
            <div className="max-w-2xl">
              <div className="mb-4 inline-flex items-center rounded-full border border-cyan-400/30 bg-cyan-500/10 px-3 py-1 text-sm font-medium text-cyan-200">
                <span className="mr-2 text-base">🛰️</span>
                Synapse Logistics • Live Negotiation Command Center
              </div>
              <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
                Coordinate disruption response with AI-powered clarity.
              </h1>
              <p className="mt-3 text-base leading-7 text-slate-300 sm:text-lg">
                Watch logistics, finance, and mediation agents negotiate in real time to land a resilient execution plan.
              </p>
            </div>

            <div className={`inline-flex items-center rounded-full px-4 py-2 text-sm font-medium ${connected ? 'bg-emerald-500/15 text-emerald-200 ring-1 ring-emerald-400/30' : 'bg-rose-500/15 text-rose-200 ring-1 ring-rose-400/30'}`}>
              <span className={`mr-2 h-2.5 w-2.5 rounded-full ${connected ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'}`} />
              {connected ? 'Connected to server' : 'Disconnected'}
            </div>
          </div>
        </header>

        <section className="rounded-[24px] border border-slate-800/70 bg-slate-950/70 p-5 shadow-[0_20px_60px_rgba(0,0,0,0.28)] backdrop-blur-xl">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
              <select
                value={selectedScenario}
                onChange={(e) => setSelectedScenario(e.target.value)}
                className="rounded-xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-slate-100 outline-none ring-0 transition focus:border-cyan-400"
                disabled={isRunning}
              >
                <option value="hurricane_port_2024">🌀 Hurricane Port Closure</option>
                <option value="budget_cut_mid_shipment">💸 Budget Cut Crisis</option>
                <option value="holiday_capacity_crunch">🎄 Holiday Capacity Crunch</option>
              </select>

              <button
                onClick={startNegotiation}
                disabled={!connected || isRunning}
                className={`rounded-xl px-5 py-3 text-sm font-semibold transition ${connected && !isRunning ? 'bg-gradient-to-r from-cyan-500 to-violet-500 text-white shadow-lg shadow-cyan-500/20 hover:brightness-110' : 'cursor-not-allowed bg-slate-800 text-slate-400'}`}
              >
                {isRunning ? '⏳ Negotiating...' : '🚀 Launch negotiation'}
              </button>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900/70 px-4 py-3 text-sm text-slate-300">
              <div className="font-medium text-slate-100">{status}</div>
              <div className="mt-1 text-slate-400">Scenario intelligence stream active</div>
            </div>
          </div>
        </section>

        <main className="grid gap-6 lg:grid-cols-3">
          <section className="rounded-[24px] border border-cyan-400/20 bg-slate-950/70 p-4 shadow-[0_16px_40px_rgba(8,145,178,0.15)] backdrop-blur-xl">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-cyan-100">🚚 Logistics Chief</h2>
              <span className="rounded-full border border-cyan-400/20 bg-cyan-500/10 px-2.5 py-1 text-xs text-cyan-200">Speed-first</span>
            </div>
            <div className="space-y-3 min-h-[420px] overflow-y-auto pr-1">
              {debateLog.filter((entry) => entry.agent === 'logistics_chief').length === 0 && !isRunning && (
                <div className="rounded-2xl border border-dashed border-slate-700 bg-slate-900/60 p-4 text-center text-sm text-slate-400">
                  Waiting for the first logistics recommendation.
                </div>
              )}
              {debateLog
                .filter((entry) => entry.agent === 'logistics_chief')
                .map((entry, idx) => (
                  <div key={idx} className={`rounded-2xl border-l-4 p-3 ${getAgentColor(entry.agent)}`}>
                    <div className="mb-2 text-[11px] uppercase tracking-[0.2em] text-slate-400">Round {entry.round}</div>
                    <p className="text-sm leading-6 text-slate-100">{entry.message}</p>
                  </div>
                ))}
            </div>
          </section>

          <section className="rounded-[24px] border border-emerald-400/20 bg-slate-950/70 p-4 shadow-[0_16px_40px_rgba(16,185,129,0.15)] backdrop-blur-xl">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-emerald-100">💰 CFO</h2>
              <span className="rounded-full border border-emerald-400/20 bg-emerald-500/10 px-2.5 py-1 text-xs text-emerald-200">Cost-sensitive</span>
            </div>
            <div className="space-y-3 min-h-[420px] overflow-y-auto pr-1">
              {debateLog.filter((entry) => entry.agent === 'cfo').length === 0 && !isRunning && (
                <div className="rounded-2xl border border-dashed border-slate-700 bg-slate-900/60 p-4 text-center text-sm text-slate-400">
                  The finance view will appear here once the negotiation starts.
                </div>
              )}
              {debateLog
                .filter((entry) => entry.agent === 'cfo')
                .map((entry, idx) => (
                  <div key={idx} className={`rounded-2xl border-l-4 p-3 ${getAgentColor(entry.agent)}`}>
                    <div className="mb-2 text-[11px] uppercase tracking-[0.2em] text-slate-400">Round {entry.round}</div>
                    <p className="text-sm leading-6 text-slate-100">{entry.message}</p>
                  </div>
                ))}
            </div>
          </section>

          <section className="rounded-[24px] border border-violet-400/20 bg-slate-950/70 p-4 shadow-[0_16px_40px_rgba(139,92,246,0.15)] backdrop-blur-xl">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-violet-100">⚖️ Operations Director</h2>
              <span className="rounded-full border border-violet-400/20 bg-violet-500/10 px-2.5 py-1 text-xs text-violet-200">Mediator</span>
            </div>
            <div className="space-y-3 min-h-[420px] overflow-y-auto pr-1">
              {debateLog.filter((entry) => entry.agent === 'mediator').length === 0 && !isRunning && (
                <div className="rounded-2xl border border-dashed border-slate-700 bg-slate-900/60 p-4 text-center text-sm text-slate-400">
                  The final ruling will appear here once the agents converge.
                </div>
              )}
              {debateLog
                .filter((entry) => entry.agent === 'mediator')
                .map((entry, idx) => (
                  <div key={idx} className={`rounded-2xl border-l-4 p-3 ${getAgentColor(entry.agent)}`}>
                    <div className="mb-2 text-[11px] uppercase tracking-[0.2em] text-slate-400">Ruling</div>
                    <p className="text-sm leading-6 text-slate-100">{entry.message}</p>
                  </div>
                ))}

              {finalPlan && (
                <div className="mt-3 rounded-[20px] border border-violet-400/30 bg-gradient-to-br from-violet-950/90 to-slate-900/90 p-4">
                  <div className="mb-3 flex items-center justify-between">
                    <h3 className="text-sm font-semibold uppercase tracking-[0.25em] text-violet-200">Final execution plan</h3>
                    {finalPlan.forced && <span className="rounded-full bg-amber-500/15 px-2.5 py-1 text-[11px] text-amber-200">Forced ruling</span>}
                  </div>

                  <div className="space-y-3 text-sm">
                    <div className="rounded-xl border border-white/10 bg-black/20 p-3">
                      <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Shipping mode</div>
                      <div className="mt-1 font-semibold text-white">{finalPlan.shipping_mode}</div>
                    </div>
                    <div className="grid gap-3 sm:grid-cols-2">
                      <div className="rounded-xl border border-white/10 bg-black/20 p-3">
                        <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Cost</div>
                        <div className="mt-1 font-semibold text-emerald-300">${Number(finalPlan.total_cost ?? 0).toLocaleString()}</div>
                      </div>
                      <div className="rounded-xl border border-white/10 bg-black/20 p-3">
                        <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Delivery time</div>
                        <div className="mt-1 font-semibold text-cyan-300">{finalPlan.delivery_time} days</div>
                      </div>
                    </div>
                    <div className="rounded-xl border border-white/10 bg-black/20 p-3 text-sm leading-6 text-slate-300">
                      {finalPlan.rationale}
                    </div>
                  </div>

                  {baseline && (
                    <div className="mt-4 rounded-xl border border-white/10 bg-black/20 p-3">
                      <div className="mb-2 text-[11px] uppercase tracking-[0.2em] text-slate-400">Vs baseline</div>
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-slate-300">Baseline cost</span>
                        <span className="text-rose-300 line-through">${baseline.single_agent_cost.toLocaleString()}</span>
                      </div>
                      <div className="mt-2 flex items-center justify-between text-sm">
                        <span className="text-slate-300">Synapse plan</span>
                        <span className="font-semibold text-emerald-300">${baseline.multi_agent_cost.toLocaleString()}</span>
                      </div>
                      <div className="mt-3 flex items-center gap-2 text-xs">
                        <span className="rounded-full bg-emerald-500/15 px-2.5 py-1 text-emerald-200">↓ {baseline.improvement_percent}% better</span>
                        <span className={`rounded-full px-2.5 py-1 ${baseline.constraints_met ? 'bg-emerald-500/15 text-emerald-200' : 'bg-rose-500/15 text-rose-200'}`}>
                          {baseline.constraints_met ? 'Constraints met' : 'Constraint risk'}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </section>
        </main>

        <footer className="text-center text-sm text-slate-400">
          <p>Synapse Logistics • AI Negotiation Command Center</p>
          <p className="mt-1">Powered by Qwen + LangGraph + FastAPI + Next.js</p>
        </footer>
      </div>
      <div ref={debateEndRef} />
    </div>
  );
}

        {/* Column 2: CFO */}
        <div className="bg-gray-800 rounded-xl p-4 border-t-4 border-green-500">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <span className="text-2xl">💰</span> CFO
          </h2>
          <div className="space-y-3 min-h-[400px] overflow-y-auto">
            {debateLog
              .filter(entry => entry.agent === 'cfo')
              .map((entry, idx) => (
                <div 
                  key={idx}
                  className={`p-3 rounded-lg border-l-4 ${getAgentColor(entry.agent)}`}
                >
                  <div className="flex items-center gap-2 text-xs text-gray-500 mb-1">
                    <span>Round {entry.round}</span>
                  </div>
                  <p className="text-sm text-gray-800">{entry.message}</p>
                </div>
              ))}
            {debateLog.filter(e => e.agent === 'cfo').length === 0 && (
              <p className="text-gray-500 italic text-center mt-8">
                Awaiting Logistics position...
              </p>
            )}
          </div>
        </div>

        {/* Column 3: Mediator / Final Plan */}
        <div className="bg-gray-800 rounded-xl p-4 border-t-4 border-purple-500">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <span className="text-2xl">⚖️</span> Operations Director (Mediator)
          </h2>
          
          <div className="space-y-3 min-h-[400px] overflow-y-auto">
            {/* Show mediator statements during debate */}
            {debateLog
              .filter(entry => entry.agent === 'mediator')
              .map((entry, idx) => (
                <div 
                  key={idx}
                  className={`p-3 rounded-lg border-l-4 ${getAgentColor(entry.agent)}`}
                >
                  <div className="flex items-center gap-2 text-xs text-gray-500 mb-1">
                    <span>Ruling</span>
                  </div>
                  <p className="text-sm text-gray-800">{entry.message}</p>
                </div>
              ))}
            
            {/* Show final plan when ready */}
            {finalPlan && (
              <div className="mt-4 p-4 bg-gradient-to-br from-purple-900 to-indigo-900 rounded-lg border-2 border-purple-400">
                <h3 className="font-bold text-lg mb-3 text-center">
                  ✅ FINAL EXECUTION PLAN
                </h3>
                
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-300">Shipping Mode:</span>
                    <span className="font-bold capitalize text-white">{finalPlan.shipping_mode}</span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-gray-300">Total Cost:</span>
                    <span className="font-bold text-green-400">${finalPlan.total_cost.toLocaleString()}</span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-gray-300">Delivery Time:</span>
                    <span className="font-bold text-blue-400">{finalPlan.delivery_time} days</span>
                  </div>
                  
                  <div className="mt-3 pt-3 border-t border-purple-700">
                    <p className="text-xs text-gray-400 italic">{finalPlan.rationale}</p>
                  </div>
                  
                  {finalPlan.forced && (
                    <div className="mt-2 px-2 py-1 bg-yellow-900 text-yellow-300 text-xs rounded text-center">
                      ⚡ Forced Compromise Ruling (Max rounds reached)
                    </div>
                  )}
                </div>
                
                {/* Baseline comparison badge */}
                {baseline && (
                  <div className="mt-4 p-3 bg-black bg-opacity-30 rounded-lg">
                    <h4 className="text-xs font-bold text-gray-400 mb-2">VS SINGLE-AGENT BASELINE</h4>
                    
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div>
                        <div className="text-gray-500">Baseline Cost</div>
                        <div className="text-red-400 line-through">
                          ${baseline.single_agent_cost.toLocaleString()}
                        </div>
                      </div>
                      
                      <div>
                        <div className="text-gray-500">Multi-Agent Cost</div>
                        <div className="text-green-400 font-bold">
                          ${baseline.multi_agent_cost.toLocaleString()}
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-2 text-center">
                      <span className="inline-block px-3 py-1 bg-green-600 text-white rounded-full text-xs font-bold">
                        ↓ {baseline.improvement_percent}% BETTER
                      </span>
                      <span className={`ml-2 inline-block px-2 py-1 rounded text-xs ${
                        baseline.constraints_met ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'
                      }`}>
                        {baseline.constraints_met ? '✅ Constraints Met' : '❌ Violation'}
                      </span>
                    </div>
                  </div>
                )}
              </div>
            )}
            
            {!finalPlan && debateLog.length === 0 && (
              <p className="text-gray-500 italic text-center mt-8">
                Final plan will appear here...
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="max-w-6xl mx-auto mt-8 text-center text-gray-500 text-sm">
        <p>Supply Chain Crisis Room • Global AI Hackathon • Agent Society Track</p>
        <p className="mt-1">Powered by Qwen (Alibaba Cloud) + LangGraph + FastAPI + Next.js</p>
      </div>
      
      <div ref={debateEndRef} />
    </div>
  );
}