# llm_server_file.py
import json
import time
from pathlib import Path
from datetime import datetime

class LLMServer:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.req_dir = self.base_dir / "requests"
        self.resp_dir = self.base_dir / "responses"
        self.done_dir = self.base_dir / "done"
        for d in (self.req_dir, self.resp_dir, self.done_dir):
            d.mkdir(parents=True, exist_ok=True)

    def _handle_request(self, req_path: Path) -> None:
        with req_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        prompt = data.get("prompt", "")
        req_id = data.get("id", req_path.stem)

        # Mock response (connectivity test)
        response_text = (
            "[LLMServer mock reply]\n"
            f"Timestamp: {datetime.utcnow().isoformat()}Z\n"
            f"Prompt length: {len(prompt)} chars"
        )

        out = {"id": req_id, "response": response_text}

        resp_path = self.resp_dir / f"{req_id}.json"
        with resp_path.open("w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

        # Move processed request so we don't re-handle it
        req_path.rename(self.done_dir / req_path.name)

    def serve_forever(self, poll_interval: float = 0.2) -> None:
        print(f"LLMServer(file) watching: {self.req_dir}")
        while True:
            for req_path in sorted(self.req_dir.glob("*.json")):
                try:
                    self._handle_request(req_path)
                except Exception as e:
                    print(f"Error handling {req_path.name}: {e}")
            time.sleep(poll_interval)

if __name__ == "__main__":
    # Choose a shared folder both terminal + notebook can read/write.
    # Example: your course repo folder or a folder in $HOME.
    server = LLMServer(base_dir="./llm_bridge")
    server.serve_forever()
