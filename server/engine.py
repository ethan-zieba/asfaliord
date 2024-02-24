import server_database
import pandas
import json


class ServerEngine(server_database.ServerDatabase):
    def __init__(self):
        super().__init__()

    def request_messages(self, username):
        permissions_level = self.read_user(self.get_user_id(username))[5]
        # messages_list is a list of tuple returned by a mysql.cursor.fetchall(),
        # each tuple containing the columns of the messages table
        messages_list = self.read_all_messages(permissions_level)
        data = {}
        for message in messages_list:
            # We get the channel in which the message was sent by searching for the last column in the row
            # (in python, this means the last item in the tuple)
            sent_in_channel = message[len(message)-1]
            try:
                # We try to append the message to the list at the specific key in data
                data[sent_in_channel].append(str(message))
            except KeyError:
                # If data[sent_in_channel] is non-existent/is not a list:
                data[sent_in_channel] = [str(message)]
        json_string = json.dumps(data)
        return json_string
