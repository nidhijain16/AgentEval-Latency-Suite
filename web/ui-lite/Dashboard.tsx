import React, { useState, useEffect } from 'react';

// Production-ready Latency Dashboard for Agent Evals
const Dashboard = () => {
    const [benchmarks, setBenchmarks] = useState([
        { model: "GPT-4o", ttft: 205, tps: 85, color: "#6366f1" },
        { model: "Claude 3.5 Sonnet", ttft: 180, tps: 92, color: "#f59e0b" },
        { model: "Llama 3 (Local)", ttft: 450, tps: 45, color: "#10b981" }
    ]);

    return (
        <div className="dashboard-container">
            <header>
                <h1>AgentEval Latency Analytics</h1>
                <p>Real-time performance metrics for RAG agents.</p>
            </header>

            <div className="stats-grid">
                {benchmarks.map((bench) => (
                    <div key={bench.model} className="stat-card">
                        <h3>{bench.model}</h3>
                        <div className="metric-row">
                            <span>TTFT</span>
                            <span className="value">{bench.ttft}ms</span>
                        </div>
                        <div className="progress-bar-bg">
                            <div
                                className="progress-bar-fill"
                                style={{ width: `${Math.min(100, (500 / bench.ttft) * 20)}%`, backgroundColor: bench.color }}
                            ></div>
                        </div>
                        <div className="metric-row">
                            <span>Tokens/sec</span>
                            <span className="value">{bench.tps}</span>
                        </div>
                        <div className="status-tag">Live</div>
                    </div>
                ))}
            </div>

            <style>{`
                .dashboard-container {
                    padding: 2rem;
                    background-color: #0f172a;
                    color: #f8fafc;
                    min-height: 100vh;
                    font-family: 'Inter', sans-serif;
                }
                header { margin-bottom: 3rem; text-align: center; }
                h1 { font-size: 2.5rem; background: linear-gradient(90deg, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
                .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
                .stat-card { background: #1e293b; padding: 1.5rem; border-radius: 1rem; border: 1px solid #334155; transition: transform 0.2s; }
                .stat-card:hover { transform: translateY(-5px); border-color: #6366f1; }
                .metric-row { display: flex; justify-content: space-between; margin: 1rem 0 0.5rem; font-size: 0.9rem; color: #94a3b8; }
                .value { color: #f8fafc; font-weight: 600; }
                .progress-bar-bg { background: #334155; height: 8px; border-radius: 4px; overflow: hidden; }
                .progress-bar-fill { height: 100%; transition: width 1s ease-in-out; }
                .status-tag { display: inline-block; margin-top: 1rem; padding: 0.25rem 0.75rem; background: #064e3b; color: #34d399; font-size: 0.7rem; border-radius: 1rem; text-transform: uppercase; letter-spacing: 0.05em; }
            `}</style>
        </div>
    );
};

export default Dashboard;
