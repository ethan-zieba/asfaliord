import http.server


class Server(http.server.HTTPServer):
    def __init__(self, ip, port):
        super().__init__((ip, port), Handler)
        self.serve_forever()


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        print("Get request")
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        print(f"POST request:\nHeaders: {self.headers}\nDate: {data.decode('utf-8')}")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()


if __name__ == "__main__":
    server = Server("127.0.0.1", 8080)