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

    def authenticate(self):
        self.authentication = requests.post(self.url, data={"username": self.username, "password": self.password}, proxies=self.proxies)
        print(self.authentication.status_code)

    def get_messages(self):
        self.response = requests.get(self.url, proxies=self.proxies)
        print(self.response.status_code)

    def send_message(self, message):
        self.message = requests.post(self.url, data={"message":message}, proxies=self.proxies)


if __name__ == "__main__":
    import credentials
    client = Client(credentials.username, credentials.password, credentials.tor_address)
    client.get_messages()
    client.authenticate()
    client.send_message("Ceci est un message test")