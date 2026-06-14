from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok", "service": "dev-practice-api"})
        elif self.path == "/api/orders":
            self.send_json(
                200,
                {
                    "orders": [
                        {"id": 1001, "status": "paid", "total": 129.9},
                        {"id": 1002, "status": "pending", "total": 59.0},
                    ]
                },
            )
        elif self.path == "/api/orders/slow":
            time.sleep(0.8)
            self.send_json(200, {"status": "ok", "warning": "response is slow"})
        else:
            self.send_json(404, {"error": "not found", "path": self.path})

    def send_json(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("Mock API running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    server.serve_forever()
