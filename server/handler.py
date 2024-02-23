import json
import uuid
from http.server import BaseHTTPRequestHandler
from http import cookies
import credentials


class Handler(BaseHTTPRequestHandler):

    active_sessions = {}

    def do_GET(self):
        # Add spamming prevention

        if self.path == '/get-messages': # Here make it so that each client has its own page with its username/session_id
            if 'Cookie' in self.headers:
                cookie = cookies.SimpleCookie(self.headers['Cookie'])
                if 'session_id' in cookie:
                    session_id = cookie['session_id'].value
                    print(f"-------------\n\nGET REQUEST FROM SESSION_ID: {session_id}")
                    print(f"ACTIVE SESSIONS: {self.__class__.active_sessions}")
                    if session_id in self.__class__.active_sessions:
                        # Encapsulate this in a different method, perhaps a different class even ?
                        print(f"{self.__class__.active_sessions[session_id]} has requested all of the messages")
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
        # Add spamming prevention

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_dict = dict(data.split('=') for data in post_data.split('&'))

        if self.path == "/login":
            username = post_dict.get('username', '')
            password = post_dict.get('password', '')

            if username in credentials.users and password == credentials.users[username]:
                print(f"-------------\n\nPOST request:\nHEADERS: {self.headers}DATA: {post_data}")
                print(f"POST DATA DICT: {post_dict}")

                # This block checks if the user already has an id
                # Note for myself: improve this code readability by putting this in another method
                has_a_cookie = False
                existing_session_id = 0
                for s_id in self.__class__.active_sessions:
                    if self.__class__.active_sessions[s_id] == username:
                        has_a_cookie = True
                        existing_session_id = s_id
                auth_cookie = cookies.SimpleCookie()

                if not has_a_cookie:
                    # Create unique session id and stores it into a cookie
                    session_id = str(uuid.uuid4())
                    auth_cookie['session_id'] = session_id

                    # Stores the session id into the active_sessions dict
                    self.__class__.active_sessions[session_id] = username
                    print(f"ACTIVE SESSIONS: {self.__class__.active_sessions}")
                    print(f"SESSION ID: {str(session_id)}")
                else:
                    auth_cookie['session_id'] = existing_session_id

                self.send_response(200)
                self.send_header('Set-Cookie', auth_cookie.output(header='', sep=''))
                self.end_headers()
                print(f"AUTH_COOKIE: {str(auth_cookie)}")
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write('Authentication failed'.encode('utf-8'))
        elif self.path == "/send-message ":
            # Here we have to check if cookie exists, if not, return 404, else return what the POST wants
            if 'Cookie' in self.headers:
                cookie = cookies.SimpleCookie(self.headers['Cookie'])
                if 'session_id' in cookie:
                    session_id = cookie['session_id'].value
                    print(f"-------------\n\nPOST REQUEST FROM SESSION_ID: {session_id}")
                    print(f"ACTIVE SESSIONS: {self.__class__.active_sessions}")
                    if session_id in self.__class__.active_sessions:
                        print(f"{self.__class__.active_sessions[session_id]} has sent a message")
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length).decode('utf-8')
                        message_data = json.loads(post_data)
                        message = message_data.get('message', '')
                        print(f"RECEIVED MESSAGE: {message}")
                        self.send_response(200)
                        self.end_headers()
            self.send_response(401)
            self.end_headers()
            self.wfile.write('AUTHENTICATION ERROR'.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Not found'.encode('utf-8'))