import uuid
from http.server import BaseHTTPRequestHandler
from http import cookies
import credentials


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.active_sessions = {}
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        if self.path == '/messages':
            if 'Cookie' in self.headers:
                cookie = cookies.SimpleCookie(self.headers['Cookie'])
                if 'session_id' in cookie:
                    session_id = cookie['session_id'].value
                    if session_id in self.active_sessions:
                        print(f"{self.active_sessions[session_id]} has requested all of the messages")
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write("Messages blablabla".encode('utf-8'))
                        return
            self.send_response(401)
            self.end_headers()
            self.wfile.write("Unauthorized".encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f"ERROR: \'{self.path}\' path not found".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_dict = dict(data.split('=') for data in post_data.split('&'))

        if self.path == "/login":
            username = post_dict.get('username', '')
            password = post_dict.get('password', '')

            if username in credentials.users and password == credentials.users[username]:
                print(f"POST request:\nHEADERS: {self.headers}DATA: {post_data}")
                print(f"POST DATA DICT: {post_dict}")

                # Create unique session id and stores it into a cookie
                session_id = str(uuid.uuid4())
                auth_cookie = cookies.SimpleCookie()
                auth_cookie['session_id'] = session_id

                # Stores the session id into the active_sessions dict
                self.active_sessions[session_id] = username
                print(f"SESSION ID: {str(session_id)}")

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                print(f"AUTH_COOKIE: {str(auth_cookie)}")
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write('Authentication failed'.encode('utf-8'))
        else:
            # Here we have to check if cookie exists, if not, return 404, else return what the POST wants
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Not found'.encode('utf-8'))