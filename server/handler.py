import uuid
from http.server import BaseHTTPRequestHandler
from http import cookies
from argon2 import PasswordHasher
from engine import ServerEngine


class Handler(BaseHTTPRequestHandler):

    active_sessions = {}
    server_engine = ServerEngine()
    users = server_engine.get_users()

    #SETTINGS RELATED TO PASSWORD HASHING
    PEPPER = "CHANGE_THIS"
    MEMORY_COST = 4000000
    TIME_COST = 1000000
    PARALLELISM = 4


    def do_GET(self):
        # Add spamming prevention

        if self.path == '/get-messages':
            if self.valid_auth_cookie():
                # Content is in the form of a dict of lists: each key is the channel id, and its value is a list of
                # the messages
                session_id = self.headers['Cookie'].split("=")[1]
                # Here we get the id of the client that asked for the messages
                print(session_id)
                # And find its username in our active sessions for better database manipulation
                content = self.server_engine.request_messages(
                    self.__class__.active_sessions[session_id])
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write('Unauthorized'.encode('utf-8'))
        elif self.path == '/get-channels':
            if self.valid_auth_cookie():
                # Content is in the form of a dict: each key is the channel id and its value is the channel's name
                # Here we find the session_id of the user so we can get its username and then the channels he has access to
                session_id = self.headers['Cookie'].split("=")[1]
                channels = self.server_engine.request_channels(self.__class__.active_sessions[session_id])
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(channels.encode('utf-8'))
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write('Unauthorized'.encode('utf-8'))
        elif self.path == "/get-server-infos":
            if self.valid_auth_cookie():
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'La Plateforme - Server for oral presentation, 3 channels available: Lounge, '
                                 b'Private Lounge and Extremely Private')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f'ERROR: \'{self.path}\' path not found'.encode('utf-8'))

    def do_POST(self):
        # Add spamming prevention in the future

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_dict = dict(data.split('=') for data in post_data.split('&'))

        if self.path == '/login':
            username = post_dict.get('username', '')
            pwd = post_dict.get('password', '')
            password = self.hash_password(pwd)

            # Updates users dict
            self.users = self.server_engine.get_users()
            if username in self.users and password == self.users[username]:
                print(f'-------------\n\nPOST request:\nHEADERS: {self.headers}DATA: {post_data}')
                print(f'POST DATA DICT: {post_dict}')
                print(f'CURRENT USERS LIST: {self.users}')
                auth_cookie = self.create_auth_cookie(username)
                self.send_response(200)
                self.send_header('Set-Cookie', auth_cookie.output(header='', sep=''))
                self.end_headers()
                print(f'AUTH_COOKIE: {str(auth_cookie)}')
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write('Authentication failed'.encode('utf-8'))

        elif self.path == '/send-message':
            # Here we have to check if cookie exists, if not, return 404, else return what the POST wants
            if self.valid_auth_cookie():
                username = self.__class__.active_sessions[self.headers['Cookie'].split("=")[1]]
                message = post_dict.get('message')
                print(f'RECEIVED MESSAGE RAW: {message} FROM: {username}')
                self.send_response(200)
                self.end_headers()
                channel_id, message = message.split('C', 1)
                self.server_engine.save_message(username, message, channel_id)
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write('AUTHENTICATION ERROR'.encode('utf-8'))

        elif self.path == '/create-account':
            username = post_dict.get('username', '')
            password = self.hash_password(post_dict.get('password', ''))
            gpg = post_dict.get('gpg', '')
            self.server_engine.create_user_if_not_exists(username, password, gpg)
            self.send_response(200)
            self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Not found'.encode('utf-8'))

    # This method creates an authentication cookie, and erases the old one if the user had one
    def create_auth_cookie(self, username):
        # This block checks if the user already has an id
        has_a_cookie = False
        existing_session_id = 0
        for s_id in self.__class__.active_sessions:
            if self.__class__.active_sessions[s_id] == username:
                has_a_cookie = True
                existing_session_id = s_id
        auth_cookie = cookies.SimpleCookie()

        # Here do the opposite: if client has a cookie already, erase it and create a new one
        # If it doesn't have a cookie: create one
        if has_a_cookie:
            del self.__class__.active_sessions[existing_session_id]
            # Create unique session id and stores it into a cookie
        session_id = str(uuid.uuid4())
        auth_cookie['session_id'] = session_id

        # Stores the session id into the active_sessions dict
        self.__class__.active_sessions[session_id] = username
        print(f'ACTIVE SESSIONS: {self.__class__.active_sessions}')
        print(f'SESSION ID: {str(session_id)}')

        return auth_cookie

    def valid_auth_cookie(self):
        if 'Cookie' in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers['Cookie'])
            if 'session_id' in self.cookie:
                session_id = self.cookie['session_id'].value
                print(f'-------------\n\nREQUEST FROM SESSION_ID: {session_id}')
                print(f'ACTIVE SESSIONS: {self.__class__.active_sessions}')
                if session_id in self.__class__.active_sessions:
                    return True
        return False

    def hash_password(self, password):
        ph = PasswordHasher(memory_cost = self.MEMORY_COST, time_cost = TIME_COST, parallelism = PARALLELISM)
        hashed_password = ph.hash(password, self.PEPPER)
        return hashed_password
        
    def verify_password(password, hashed_password):
        ph = PasswordHasher(memory_cost = MEMORY_COST, time_cost = TIME_COST, parallelism = PARALLELISM)
        check = ph.verify(hashed_password, password)
        return check