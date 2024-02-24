import server_database
import pandas
import json


class ServerEngine(server_database.ServerDatabase):
    def __init__(self):
        super().__init__()

    def request_messages(self, username):
        permissions_level = self.read_user(self.get_user_id(username))[5]
        channels_accessible = self.read_all_channels(permissions_level)
        messages_number = self.database.count_messages()
        messages_list = []
        if messages_number > 100:
            pass
            # json_string = json.dumps(data)
            # self.wfile.write(json_string)
            # cursor.fetchall() returns a list of tuples with mysql connector
