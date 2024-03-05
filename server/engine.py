import server_database
import json
import datetime


class ServerEngine(server_database.ServerDatabase):
    def __init__(self):
        super().__init__()

    def request_messages(self, username):
        self.open_connection()
        permissions_level = self.read_user(self.get_user_id(username))[4]
        # messages_list is a list of tuple returned by a mysql.cursor.fetchall(),
        # each tuple containing the columns of the messages table
        messages_list = self.read_all_messages(permissions_level)
        data = {}
        for message in messages_list:
            # We get the channel in which the message was sent by searching for the last column in the row
            # (in python, this means the last item in the tuple)
            sent_in_channel = str(message[len(message)-2])
            content = message[1]
            try:
                # We try to append the message to the list at the specific key in data
                data[sent_in_channel].append(str(content))
            except KeyError:
                # If data[sent_in_channel] is non-existent/is not a list:
                data[sent_in_channel] = [str(content)]
        json_string = json.dumps(str(data))
        self.close_connection()
        return json_string

    def save_message(self, username, message):
        self.open_connection()
        self.create_message(1,
                            f"{datetime.date.today().strftime('%Y/%m/%d')} - {username} - {message}", "2025-10-10")
        self.close_connection()
