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

    def get_channels(self):
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


if __name__ == "__main__":
    import credentials
    import json
    client = Client(credentials.tor_address)
    client.authenticate(credentials.username, credentials.password)
    print("\n\n\n")
    messages = client.get_messages()
    print(json.loads(messages), type(json.loads(messages)))
