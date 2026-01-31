from http.server import BaseHTTPRequestHandler, HTTPServer


HOST = "0.0.0.0"
PORT = 8080


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from Docker! Your app is running with second tag:latest .\n")


if __name__ == "__main__":
    print(f"Server starting on {HOST}:{PORT}")
    HTTPServer((HOST, PORT), SimpleHandler).serve_forever()
