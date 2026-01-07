# llm_server_file.py
from __future__ import annotations

import json
import time
from pathlib import Path

from openai_adapter import OpenAIAdapter


class LLMServer:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir).resolve()
        self.req_dir = self.base_dir / "requests"
        self.resp_dir = self.base_dir / "responses"
        self.done_dir = self.base_dir / "done"
        for d in (self.req_dir, self.resp_dir, self.done_dir):
            d.mkdir(parents=True, exist_ok=True)

        self.llm = OpenAIAdapter()

        print(f"[LLMServer] base_dir = {self.base_dir}")
        print(f"[LLMServer] watching  = {self.req_dir}")

    def _handle_request(self, req_path: Path) -> None:
        with req_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        req_id = data["id"]
        prompt = data.get("prompt", "")

        # Pedagogically meaningful parameters
        model = data.get("model", "gpt-4o-mini")
        temperature = data.get("temperature", 0.2)
        max_output_tokens = data.get("max_output_tokens", 200)
        instructions = data.get("instructions", None)

        try:
            text = self.llm.generate(
                model=model,
                prompt=prompt,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                instructions=instructions,
                store=False,
            )
            out = {"id": req_id, "ok": True, "response": text}
        except Exception as e:
            out = {"id": req_id, "ok": False, "error": repr(e)}

        resp_path = self.resp_dir / f"{req_id}.json"
        with resp_path.open("w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

        # Move processed request aside
        req_path.rename(self.done_dir / req_path.name)

    def serve_forever(self, poll_interval: float = 0.2) -> None:
        while True:
            for req_path in sorted(self.req_dir.glob("*.json")):
                self._handle_request(req_path)
            time.sleep(poll_interval)


if __name__ == "__main__":
    # Use an ABSOLUTE path in practice for fewer surprises
    server = LLMServer(base_dir="./llm_bridge")
    server.serve_forever()
