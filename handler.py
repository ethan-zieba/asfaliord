from http.server import BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        print("Get request")
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        print(f"POST request:\nHEADERS: {self.headers}\nDATA: {data.decode('utf-8')}")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()