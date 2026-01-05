# llm_client.py
import requests

class LLMClient:
    def __init__(self, base_url="http://127.0.0.1:8000", timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def health(self):
        r = requests.get(
            f"{self.base_url}/health",
            timeout=self.timeout
        )
        r.raise_for_status()
        return r.json()

    def prompt(self, prompt_text: str) -> str:
        payload = {
            "prompt": prompt_text
        }

        r = requests.post(
            f"{self.base_url}/prompt",
            json=payload,
            timeout=self.timeout
        )
        r.raise_for_status()
        return r.json()["response"]
