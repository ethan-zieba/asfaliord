import requests


class Client:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
        self.session = requests.session()
        self.proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
        }
        self.cookie = None

    def authenticate(self):
        data = {"username": self.username, "password": self.password}
        print(f"ASKING FOR AUTH_COOKIE, DATA: {data}")
        response = self.session.post(f"{self.url}/login", data=data, proxies=self.proxies)
        print(f"Authentication status: {response.status_code}")
        if response.status_code == 200:
            self.cookie = response.cookies.get('session_id')
            print(f"STORED COOKIES: {self.cookie}")

    def get_messages(self):
        if hasattr(self, 'cookie'):
            headers = {'Cookie': f'session_id={self.cookie}'}
            print(f"ASKING FOR MESSAGES\nWITH HEADERS: {headers}\nSENDING COOKIE: {self.cookie}\nUSING PROXIES: {self.proxies}")
            response = self.session.get(f"{self.url}/messages", headers=headers, proxies=self.proxies)
            print(response.status_code)
            print(response.text)
        else:
            print("AUTHENTICATION ERROR: No auth cookie")

    def send_message(self, message):
        if hasattr(self, 'cookie'):
            headers = {'Cookie': f'session_id={self.cookie}'}
            print(f"SENDING MESSAGE\nHEADERS: {headers}\nSENDING COOKIE: {self.cookie}\nUSING PROXIES: {self.proxies}")
            response = self.session.post(f"{self.url}/send_message", data={"message":message}, headers=headers, proxies=self.proxies)
        else:
            print("AUTHENTICATION ERROR: No auth cookie")


if __name__ == "__main__":
    import credentials
    client = Client(credentials.username, credentials.password, credentials.tor_address)
    client.authenticate()
    print("\n\n\n")
    client.get_messages()
