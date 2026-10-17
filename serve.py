import http.server
import socketserver
import os
import sys

import socket

PORT = 3000
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    PORT = int(sys.argv[1])
else:
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    if is_port_in_use(PORT):
        for candidate in range(3001, 3020):
            if not is_port_in_use(candidate):
                print(f"Port {PORT} is currently in use. Switching to port {candidate}...")
                PORT = candidate
                break

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIRECTORY)

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.path = "/preview.html"
        return super().do_GET()

print(f"Starting server at http://localhost:{PORT}...")
sys.stdout.flush()

# Allow address reuse
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving GitHub Profile Preview at http://localhost:{PORT}")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
