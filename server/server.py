from http.server import HTTPServer
from handler import Handler


class Server(HTTPServer):
    def __init__(self, ip, port):
        super().__init__((ip, port), Handler)
        self.serve_forever()


if __name__ == "__main__":
    server = Server("127.0.0.1", 8080)