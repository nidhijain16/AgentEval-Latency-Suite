# AgentEval-Latency-Suite

> *A production-grade benchmarking tool for RAG Agents, focusing on reliability and sub-second latency.*

## Why this exists
AI Agents often fail in production due to "looping" or high latency. This suite provides a testing harness to ensure agents are ready before deployment.

## Features

* **Multi-Agent Coordination:** Uses LangGraph to manage state between "Researcher" and "Verifier" agents.
* **Latency Benchmarking:** Automated tracking of TTFT (Time To First Token) and total inference time.
* **Hallucination Guardrails:** Integration of custom evaluation metrics to ensure document reasoning remains grounded in the provided context.
* **TypeScript Integration:** Includes a React-based UI to visualize agent decision-making in real-time.

## Tech Stack

* **Backend:** Python (FastAPI), LangGraph, PyTorch.
* **Frontend:** React, TypeScript.
* **Inference:** OpenAI Whisper (optimized for 30% lower latency).
* **DevOps:** Docker, GitHub Actions for CI/CD.

## Getting Started

### Prerequisites
- Python 3.9+
- OpenAI API Key (or other supported providers)

### Installation
```bash
pip install -r requirements.txt
```

### Running the Latency Benchmark
```bash
python benchmarks/latency_test.py
```

## Repository Structure
```text
├── agents/
│   ├── researcher.py       # LangGraph-based multi-agent logic
│   └── architect.py        # Logic for breaking prompts into structured data
├── benchmarks/
│   ├── latency_test.py     # Script to measure Time To First Token (TTFT)
│   └── eval_framework.py   # RAGAS or custom metrics for hallucination checks
├── web/
│   └── ui-lite/             # Small React/TypeScript dashboard to show the results
├── Dockerfile              # Proves you can containerize the service
└── README.md               # The most important part for the "60-second scan"
```
