import uuid
from http.server import BaseHTTPRequestHandler
from http import cookies
from argon2 import PasswordHasher
from engine import ServerEngine
import json


class Handler(BaseHTTPRequestHandler):

    active_sessions = {}
    server_engine = ServerEngine()
    users = server_engine.get_users()
    voice_channels = {"1": ["Main"]}

    # SETTINGS RELATED TO PASSWORD HASHING
    # MEMORY_COST is the memory allocated to the hashing process, in Kibibyte
    MEMORY_COST = 99999
    # TIME_COST is the number of iterations
    TIME_COST = 6
    # PARALLELISM is the number of parallel threads
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
                # Here we find the session_id of the user, so we can get its username and then the channels he has access to
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
        elif self.path == "/get-voice-channels":
            if self.valid_auth_cookie():
                channels = self.voice_channels
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(channels).encode("utf-8"))

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
            password = post_dict.get('password', '')

            # Updates users dict
            self.users = self.server_engine.get_users()
            if username in self.users and self.verify_password(password, self.users[username]) == True :
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
                if message[2:4] == "%2F":
                    if int(self.server_engine.get_user_permission_level(username)) > 4:
                        if "create_text_channel" in message:
                            _, channel_name, channel_perm = message.split(" -")
                            self.server_engine.create_channel(channel_name, channel_perm)
                else:
                    self.server_engine.save_message(username, message, channel_id)
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write('AUTHENTICATION ERROR'.encode('utf-8'))

        elif self.path == '/send-ip':
            if self.valid_auth_cookie():
                ip = post_dict.get('ip')
                username = self.__class__.active_sessions[self.headers['Cookie'].split("=")[1]]
                channel = post_dict.get('channel')
                print(f"{username} SENDS ITS IP: {ip}\nWAITS FOR A CALL IN CHANNEL: {channel}")
                self.send_response(200)
                self.end_headers()
                self.voice_channels[channel].append(ip)

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
        # Creates PasswordHasher object from argon2 module
        ph = PasswordHasher(memory_cost = self.MEMORY_COST, time_cost = self.TIME_COST, parallelism = self.PARALLELISM)
        hashed_password = ph.hash(password)
        return hashed_password
        
    def verify_password(self, password, hashed_password):
        # Uses argon2 pre-builtin verify method
        ph = PasswordHasher(memory_cost = self.MEMORY_COST, time_cost = self.TIME_COST, parallelism = self.PARALLELISM)
        check = ph.verify(hashed_password, password)
        return check
