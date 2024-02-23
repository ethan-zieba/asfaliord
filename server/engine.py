import server_database
import pandas
import json


class ServerEngine:
    def __init__(self):
        self.database = server_database.ServerDatabase()

    def request_messages(self):
        messages_number = self.database.count_messages()
        messages_list = []
        if messages_number > 100:
            pass
            # json_string = json.dumps(data)
            # self.wfile.write(json_string)
            # cursor.fetchall() returns a list of tuples with mysql connector
