from client import Client
import credentials


# Here credentials is a .py file with testing credentials, for test version only
client = Client(credentials.username, credentials.password, credentials.tor_address)
client.authenticate()
client.get_messages()
client.send_message("This is a test message")
