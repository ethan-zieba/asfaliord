import requests


class Client:
    def __init__(self, url):
        self.url = url
        self.session = requests.session()
        self.proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
        }
        self.cookie = None

    def authenticate(self, username, password):
        data = {"username": username, "password": password}
        print(f"ASKING FOR AUTH_COOKIE, DATA: {data}")
        response = self.session.post(f"{self.url}/login", data=data, proxies=self.proxies)
        print(f"Authentication status: {response.status_code}")
        if response.status_code == 200:
            self.cookie = response.cookies.get('session_id')
            print(f"STORED COOKIES: {self.cookie}")
            return True

    def get_messages(self):
        if self.cookie != None:
            headers = {'Cookie': f'session_id={self.cookie}'}
            print(f"ASKING FOR MESSAGES\nWITH HEADERS: {headers}\nSENDING COOKIE: {self.cookie}\nUSING PROXIES: {self.proxies}")
            response = self.session.get(f"{self.url}/messages", headers=headers, proxies=self.proxies)
            print(response.status_code)
            #print(response.json())
        else:
            print("AUTHENTICATION ERROR: No auth cookie")

    def send_message(self, message):
        if self.cookie != None:
            data = {"message": message}
            headers = {'Cookie': f'session_id={self.cookie}'}
            print(f"SENDING MESSAGE\nHEADERS: {headers}\nSENDING COOKIE: {self.cookie}\nUSING PROXIES: {self.proxies}\nDATA: {data}")
            response = self.session.post(f"{self.url}/send-message", data=data, headers=headers, proxies=self.proxies)
            print(response.status_code)
        else:
            print("AUTHENTICATION ERROR: No auth cookie")


if __name__ == "__main__":
    import credentials
    client = Client(credentials.tor_address)
    client.authenticate(credentials.username, credentials.password)
    print("\n\n\n")
    client.send_message("Hello world!")
