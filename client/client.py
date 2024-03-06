import threading
import pyaudio
import socket
import requests


class Client:
    def __init__(self, url):
        self.url = url
        self.session = requests.session()
        # Using Tor proxies on client computer
        self.proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
        }
        self.cookie = None

        # Voice channel part
        self.stop_threads = False
        self.audio = pyaudio.PyAudio()
        self.input_stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                                            frames_per_buffer=1024)
        self.output_stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None

    # We use this method here instead of putting variables in __init__ so we can easily manipulate and/or remove it
    # after
    def get_host_port(self, host, port, peer_ip):
        self.host = host
        self.port = port
        self.peer_ip = peer_ip

    def start_call(self):
        self.stop_threads = False
        self.sock.connect((self.peer_ip, self.port))
        self.connection = self.sock
        # Here we call our two main audio functions using threads, so we can call them in parallel
        send_thread = threading.Thread(target=self.send_audio).start()
        receive_thread = threading.Thread(target=self.receive_audio).start()

    def stop_call(self):
        self.stop_threads = True
        self.sock.close()
        self.input_stream.stop_stream()
        self.input_stream.close()

        self.output_stream.stop_stream()
        self.output_stream.close()

        self.audio.terminate()

    def send_audio(self):
        while not self.stop_threads:
            data = self.input_stream.read(1024)
            self.connection.sendall(data)

    def receive_audio(self):
        while not self.stop_threads:
            data = self.connection.recv(1024)
            self.connection.sendall(data)

    def standby_before_call(self, tkinter_frame):
        for i in range(3):
            try:
                self.sock.bind('0.0.0.0', self.port)
                self.sock.listen(1)
                print('WAITING FOR A CALL')
                client_socket, _ = self.sock.accept()
                self.start_call()
            except Exception:
                print(f"ERROR WHILE WAITING FOR CALL: {Exception}")
                tkinter_frame.after(4000, print('TRYING AGAIN...'))

    def send_own_ip(self, channel):
        ip_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_s.connect(("8.8.8.8", 80))
        data = {"username": self.username, "ip": self.get_own_ip(), "channel": channel}
        ip_s.close()
        headers = {'Cookie': f'session_id={self.cookie}'}
        print(
            f"SENDING OWN IP\nHEADERS: {headers}\nSENDING COOKIE: {self.cookie}\nUSING PROXIES: {self.proxies}\nDATA: {data}")
        response = self.session.post(f"{self.url}/send-ip", data=data, headers=headers, proxies=self.proxies)

    def get_own_ip(self):
        ip_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_s.connect(("8.8.8.8", 80))
        ip = ip_s.getsockname()[0]
        ip_s.close()
        return ip

    def create_account(self, username, password, gpg):
        # Data to send via request
        data = {"username": username, "password": password, "gpg": gpg}
        print(f"ASKING FOR ACCOUNT CREATION, DATA: {data}")
        # Sending post request, specifying proxies to use
        response = self.session.post(f"{self.url}/create-account", data=data, proxies=self.proxies)
        print(f"Response status: {response.status_code}")
        # 200 is a success code
        if response.status_code == 200:
            print(f"ACCOUNT SUCCESSFULLY CREATED")
            return True
        return False

    def authenticate(self, username, password):
        data = {"username": username, "password": password}
        self.username = username
        print(f"ASKING FOR AUTH_COOKIE, DATA: {data}")
        # Sends a POST request for a cookie, with username and password
        response = self.session.post(f"{self.url}/login", data=data, proxies=self.proxies)
        print(f"Authentication status: {response.status_code}")
        if response.status_code == 200:
            # Stores the cookie inside the attribute self.cookie
            self.cookie = response.cookies.get('session_id')
            print(f"STORED COOKIES: {self.cookie}")
            return True
        return False

    def get_messages(self):
        if self.cookie is not None:
            headers = {'Cookie': f'session_id={self.cookie}'}
            print(f"ASKING FOR MESSAGES\nWITH HEADERS: {headers}\nSENDING COOKIE: {self.cookie}\nUSING PROXIES: {self.proxies}")
            response = self.session.get(f"{self.url}/get-messages", headers=headers, proxies=self.proxies)
            print(response.status_code)
            # Response is in a json format
            return response.json().replace("'", '"')
        else:
            print("AUTHENTICATION ERROR: No auth cookie")

    def get_voice_channels(self):
        if self.cookie is not None:
            headers = {'Cookie': f'session_id={self.cookie}'}
            print(
                f"ASKING FOR VOICE CHANNELS NAMES AND USERS\nWITH HEADERS: {headers}\nSENDING COOKIE: {self.cookie}\nUSING PROXIES: {self.proxies}")
            response = self.session.get(f"{self.url}/get-voice-channels", headers=headers, proxies=self.proxies)
            print(response.status_code)
            # Response is in a json format
            print(response.json())
            return response.json()

    def get_other_ip(self, channel_id):
        channels = self.get_voice_channels()
        other_ip = channels[channel_id][2]
        return other_ip

    def get_text_channels(self):
        if self.cookie is not None:
            headers = {'Cookie': f'session_id={self.cookie}'}
            print(f"ASKING FOR CHANNELS NAMES\nWITH HEADERS: {headers}\nSENDING COOKIE: {self.cookie}\nUSING PROXIES: {self.proxies}")
            response = self.session.get(f"{self.url}/get-channels", headers=headers, proxies=self.proxies)
            print(response.status_code)
            # Response is in a json format
            print(response.json().replace("'", '"'))
            return response.json().replace("'", '"')
        else:
            print("AUTHENTICATION ERROR: No auth cookie")

    def get_server_namedesc(self):
        if self.cookie is not None:
            headers = {'Cookie': f'session_id={self.cookie}'}
            print(f"ASKING FOR SERVER NAME\nWITH HEADERS: {headers}\nSENDING COOKIE: {self.cookie}\nUSING PROXIES: {self.proxies}")
            response = self.session.get(f"{self.url}/get-server-infos", headers=headers, proxies=self.proxies)
            print(response.status_code)
            print(response.text)
            return response.text
        else:
            print("AUTHENTICATION ERROR: No auth cookie")

    def send_message(self, message, channel):
        if self.cookie is not None:
            message = f"{channel}C{message}"
            data = {"message": message}
            headers = {'Cookie': f'session_id={self.cookie}'}
            print(f"SENDING MESSAGE\nHEADERS: {headers}\nSENDING COOKIE: {self.cookie}\nUSING PROXIES: {self.proxies}\nDATA: {data}")
            response = self.session.post(f"{self.url}/send-message", data=data, headers=headers, proxies=self.proxies)
            print(response.status_code)
        else:
            print("AUTHENTICATION ERROR: No auth cookie")

    def get_users(self):
        if self.cookie is not None:
            headers = {'Cookie': f'session_id={self.cookie}'}
            response = self.session.get(f"{self.url}/get-users", headers=headers, proxies=self.proxies)
            return response.json()


if __name__ == "__main__":
    import credentials
    import json
    client = Client(credentials.tor_address)
    client.get_host_port('127.0.0.1', 25567, credentials.other_ip)
    client.start_call()
