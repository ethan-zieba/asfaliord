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
        self.cookies = None

    def authenticate(self):
        data = {"username": self.username, "password": self.password}
        self.authentication = requests.post(f"{self.url}/login", data=data, proxies=self.proxies)
        print(f"Authentication status: {self.authentication.status_code}")
        self.cookies = self.authentication.cookies
        print(f"STORED COOKIES: {self.cookies}")

    def get_messages(self):
        print(f"ASKING FOR MESSAGES\nSENDING COOKIES: {self.cookies}\nUSING PROXIES: {self.proxies}")
        self.response = requests.get(self.url, proxies=self.proxies)
        print(self.response.status_code)

    def send_message(self, message):
        self.message = requests.post(self.url, data={"message":message}, proxies=self.proxies)


if __name__ == "__main__":
    import credentials
    client = Client(credentials.username, credentials.password, credentials.tor_address)
    client.authenticate()
    client.get_messages()
    client.send_message("Ceci est un message test")