# llm_server.py
from flask import Flask, request, jsonify
from datetime import datetime

class LLMServer:
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self._register_routes()

    def _register_routes(self):
        @self.app.route("/health", methods=["GET"])
        def health():
            return jsonify(status="ok")

        @self.app.route("/prompt", methods=["POST"])
        def prompt():
            data = request.get_json()
            prompt_text = data.get("prompt", "")

            # Fake LLM response (connectivity test only)
            response_text = (
                f"[LLMServer mock reply]\n"
                f"Timestamp: {datetime.utcnow().isoformat()}Z\n"
                f"Prompt length: {len(prompt_text)} chars"
            )

            return jsonify(
                response=response_text
            )

    def run(self):
        self.app.run(host=self.host, port=self.port)


if __name__ == "__main__":
    server = LLMServer()
    server.run()
