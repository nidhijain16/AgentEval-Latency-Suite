import asyncio
import time
import json
from typing import List, Dict, Any, Optional
import httpx

class LatencyBenchmarker:
    """
    A production-grade benchmarker for LLM latency.
    Tracks Time To First Token (TTFT), tokens per second, and total inference time.
    """
    
    def __init__(self, model_name: str = "gpt-4o", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.results = []

    async def run_single_inference(self, prompt: str, user_id: int) -> Dict[str, Any]:
        """
        Runs a single streaming inference and tracks metrics.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }

        # Mock implementation for demonstration if no API key is provided
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            return await self._mock_inference(prompt, user_id)

        start_time = time.perf_counter()
        ttft = None
        total_tokens = 0
        full_response = []

        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("POST", self.base_url, headers=headers, json=data, timeout=60.0) as response:
                    async for line in response.aiter_lines():
                        if not line.strip() or line.strip() == "data: [DONE]":
                            continue
                        
                        if ttft is None:
                            ttft = time.perf_counter() - start_time
                        
                        chunk = json.loads(line.replace("data: ", ""))
                        delta = chunk["choices"][0].get("delta", {}).get("content", "")
                        if delta:
                            full_response.append(delta)
                            total_tokens += 1 # Rough estimation, real tokenizers are better

            except Exception as e:
                print(f"Error in user {user_id}: {e}")
                return {"user_id": user_id, "error": str(e)}

        end_time = time.perf_counter()
        total_time = end_time - start_time
        tps = total_tokens / (total_time - ttft) if total_time > ttft else 0

        result = {
            "user_id": user_id,
            "ttft_ms": ttft * 1000,
            "total_time_ms": total_time * 1000,
            "tokens_per_second": tps,
            "total_tokens": total_tokens,
            "status": "success"
        }
        return result

    async def _mock_inference(self, prompt: str, user_id: int) -> Dict[str, Any]:
        """
        Simulates a streaming response for testing/demonstration.
        """
        start_time = time.perf_counter()
        # Simulate network lag
        await asyncio.sleep(0.2) 
        ttft = time.perf_counter() - start_time
        
        # Simulate token generation
        for _ in range(20):
            await asyncio.sleep(0.05)
            
        end_time = time.perf_counter()
        total_time = end_time - start_time
        total_tokens = 20
        tps = total_tokens / (total_time - ttft)

        return {
            "user_id": user_id,
            "ttft_ms": ttft * 1000,
            "total_time_ms": total_time * 1000,
            "tokens_per_second": tps,
            "total_tokens": total_tokens,
            "status": "mock_success"
        }

    async def run_benchmark(self, prompts: List[str], concurrent_users: int = 5):
        """
        Runs the benchmark with multiple concurrent users.
        """
        print(f"Starting benchmark: {concurrent_users} concurrent users...")
        tasks = []
        for i in range(concurrent_users):
            prompt = prompts[i % len(prompts)]
            tasks.append(self.run_single_inference(prompt, i))
        
        self.results = await asyncio.gather(*tasks)
        self.print_summary()

    def print_summary(self):
        """
        Prints the benchmark results with statistical analysis (P50, P95, P99).
        """
        import statistics

        print("\n" + "="*70)
        print(f"{'User ID':<10} | {'TTFT (ms)':<12} | {'Total (ms)':<12} | {'TPS':<8} | {'Status'}")
        print("-" * 70)
        
        ttfts = []
        tpss = []
        valid_results = 0
        
        for r in self.results:
            if "error" in r:
                print(f"{r['user_id']:<10} | {'FAILED':<12} | {'-':<12} | {'-':<8} | {r['error'][:20]}...")
                continue
            
            print(f"{r['user_id']:<10} | {r['ttft_ms']:>10.2f} | {r['total_time_ms']:>10.2f} | {r['tokens_per_second']:>8.2f} | {r['status']}")
            ttfts.append(r['ttft_ms'])
            tpss.append(r['tokens_per_second'])
            valid_results += 1

        if valid_results > 0:
            print("-" * 70)
            print(f"Mean        | {statistics.mean(ttfts):>10.2f} | {'-':<12} | {statistics.mean(tpss):>8.2f} |")
            if valid_results > 1:
                ttfts.sort()
                p50 = statistics.median(ttfts)
                p95 = self._get_percentile(ttfts, 95)
                p99 = self._get_percentile(ttfts, 99)
                print(f"P50 (Median)| {p50:>10.2f} | (Tail Latency Analysis)")
                print(f"P95         | {p95:>10.2f} | (Production Threshold)")
                print(f"P99         | {p99:>10.2f} | (Extreme Case)")
        print("="*70 + "\n")

    def _get_percentile(self, data: List[float], percentile: float) -> float:
        """Simple percentile calculation."""
        if not data:
            return 0
        size = len(data)
        import math
        index = (percentile / 100) * (size - 1)
        lower = math.floor(index)
        upper = math.ceil(index)
        if lower == upper:
            return data[int(index)]
        weight = index - lower
        return data[lower] * (1 - weight) + data[upper] * weight

if __name__ == "__main__":
    benchmarker = LatencyBenchmarker(api_key="YOUR_API_KEY")
    prompts = [
        "Explain quantum computing in three sentences.",
        "How do I build a RAG pipeline?",
        "What is the capital of France?",
        "Write a quicksort implementation in Python.",
        "Summarize the benefits of multi-agent systems."
    ]
    
    asyncio.run(benchmarker.run_benchmark(prompts, concurrent_users=5))
