"""A local API whose responses reproduce the incident signals from lesson 012."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class IncidentHandler(BaseHTTPRequestHandler):
    """Serve one healthy endpoint and one deliberately unhealthy business endpoint."""

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler requires this name.
        if self.path == "/health":
            self.send_json(200, {"status": "ok", "service": "dev-workbench-demo"})
        elif self.path == "/api/orders":
            self.send_json(
                503,
                {
                    "error": "upstream unavailable",
                    "hint": "check the order-provider connection",
                },
            )
        else:
            self.send_json(404, {"error": "not found", "path": self.path})

    def send_json(self, status_code: int, payload: dict[str, str]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        print("%s - %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8013), IncidentHandler)
    print("Incident demo API: http://127.0.0.1:8013")
    print("Press Ctrl+C to stop.")
    server.serve_forever()
