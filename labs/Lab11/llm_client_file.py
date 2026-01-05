# llm_client_file.py
import json
import time
import uuid
from pathlib import Path

class LLMClient:
    def __init__(self, base_dir: str, timeout_s: float = 30.0, poll_interval: float = 0.2):
        self.base_dir = Path(base_dir)
        self.req_dir = self.base_dir / "requests"
        self.resp_dir = self.base_dir / "responses"
        self.req_dir.mkdir(parents=True, exist_ok=True)
        self.resp_dir.mkdir(parents=True, exist_ok=True)

        self.timeout_s = timeout_s
        self.poll_interval = poll_interval

    def prompt(self, prompt_text: str) -> str:
        req_id = str(uuid.uuid4())
        req_path = self.req_dir / f"{req_id}.json"
        resp_path = self.resp_dir / f"{req_id}.json"

        payload = {"id": req_id, "prompt": prompt_text}

        with req_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)

        # Wait for response
        deadline = time.time() + self.timeout_s
        while time.time() < deadline:
            if resp_path.exists():
                with resp_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                return data["response"]
            time.sleep(self.poll_interval)

        raise TimeoutError(f"No response after {self.timeout_s}s (req_id={req_id}).")
