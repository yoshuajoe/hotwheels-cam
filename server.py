import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server berjalan di port {PORT}")
    print(f"Buka browser dan akses http://localhost:{PORT}/hw.html")
    httpd.serve_forever() 