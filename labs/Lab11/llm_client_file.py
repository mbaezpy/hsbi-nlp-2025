# llm_client_file.py
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Optional


class LLMClient:
    def __init__(self, base_dir: str, timeout_s: float = 60.0, poll_interval: float = 0.2):
        self.base_dir = Path(base_dir).resolve()
        self.req_dir = self.base_dir / "requests"
        self.resp_dir = self.base_dir / "responses"
        self.req_dir.mkdir(parents=True, exist_ok=True)
        self.resp_dir.mkdir(parents=True, exist_ok=True)
        self.timeout_s = timeout_s
        self.poll_interval = poll_interval

    def prompt(
        self,
        prompt_text: str,
        *,
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_output_tokens: int = 200,
        instructions: Optional[str] = None,
    ) -> str:
        req_id = str(uuid.uuid4())
        req_path = self.req_dir / f"{req_id}.json"
        resp_path = self.resp_dir / f"{req_id}.json"

        payload = {
            "id": req_id,
            "prompt": prompt_text,
            "model": model,
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "instructions": instructions,
        }

        with req_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)

        deadline = time.time() + self.timeout_s
        while time.time() < deadline:
            if resp_path.exists():
                with resp_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if not data.get("ok", False):
                    raise RuntimeError(f"LLM server error: {data.get('error')}")
                return data["response"]
            time.sleep(self.poll_interval)

        raise TimeoutError(f"No response after {self.timeout_s}s (req_id={req_id}).")
