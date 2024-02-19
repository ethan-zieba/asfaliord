import uuid
from http.server import BaseHTTPRequestHandler
from http import cookies
import credentials


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.sessions = {}
        super().__init__(*args, **kwargs)
    def do_GET(self):
        self.send_response(200)
        print("Get request")
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        if self.path == "/login":
            post_dict = dict(data.split('=') for data in post_data.split('&'))
            username = post_dict.get('username', '')
            password = post_dict.get('password', '')

            if username in credentials.usernames and password == credentials[username]:
                print(f"POST request:\nHEADERS: {self.headers}\nDATA: {post_data.decode('utf-8')}")
                session_id = str(uuid.uuid4())
                self.sessions[session_id] = username
                print(str(session_id))
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                auth_cookie = cookies.SimpleCookie()
                print(str(auth_cookie))
                auth_cookie['session_id'] = session_id
                self.send_header('Set-Cookie', auth_cookie.output(header='', sep=''))
                self.wfile.write('Authentication successful'.encode('utf-8'))
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write('Authentication failed'.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Not found'.encode('utf-8'))