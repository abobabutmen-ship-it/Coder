import os
import time
import re
import requests
from typing import Tuple

REDACT_PATTERNS = [
    re.compile(r"(?:API|KEY|TOKEN)[=:]\s*([A-Za-z0-9\-_.]+)", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
]

def redact(text: str) -> str:
    if not text:
        return text
    out = text
    for p in REDACT_PATTERNS:
        out = p.sub("[REDACTED]", out)
    return out

class LLMClient:
    def __init__(self, max_retries: int = 2, backoff: float = 1.0, timeout: int = 15, cost_limit_tokens: int = 2000):
        self.api_key = os.environ.get("LLM_API_KEY")
        self.provider = os.environ.get("LLM_PROVIDER", "openai-compatible")
        self.endpoint = os.environ.get("LLM_ENDPOINT")
        self.max_retries = max_retries
        self.backoff = backoff
        self.timeout = timeout
        self.cost_limit_tokens = int(os.environ.get("LLM_COST_LIMIT", cost_limit_tokens))

    def improve_code(self, code: str, max_tokens: int = 300) -> dict:
        if not self.api_key:
            return {"improved_code": code, "notes": ["No API key configured"]}
        if max_tokens > self.cost_limit_tokens:
            return {"improved_code": code, "notes": ["Requested tokens exceed cost limit"]}

        payload = {
            "model": os.environ.get("LLM_MODEL", "gpt-4o-mini"),
            "input": f"Improve the following code, keep behaviour:\n\n{code}",
            "max_tokens": max_tokens,
        }
        url = self.endpoint or "https://api.example-llm.com/v1/generate"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        attempt = 0
        last_err = None
        while attempt <= self.max_retries:
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                improved = data.get("output") or data.get("result") or data.get("text")
                if isinstance(improved, list):
                    improved = "\n".join(improved)
                # redact just in case
                return {"improved_code": redact(improved or code), "notes": ["LLM used"]}
            except Exception as e:
                last_err = str(e)
                attempt += 1
                time.sleep(self.backoff * attempt)
        return {"improved_code": code, "notes": [f"LLM error after retries: {last_err}"]}


def LLMAvailable() -> bool:
    return bool(os.environ.get("LLM_API_KEY") and os.environ.get("LLM_PROVIDER"))
