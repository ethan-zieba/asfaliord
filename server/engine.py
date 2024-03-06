import server_database
import json
import datetime


class ServerEngine(server_database.ServerDatabase):
    def __init__(self):
        super().__init__()

    def request_messages(self, username):
        self.open_connection()
        permissions_level = self.get_user_permission_level(username)
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

    def request_channels(self, username):
        self.open_connection()
        permission_level = self.get_user_permission_level(username)
        # channels_list is a list of tuple returned by a mysql.cursor.fetchall(),
        # each tuple containing the columns of the messages table
        channels_list = self.read_all_channels(permission_level)
        data = {}
        for channel in channels_list:
            name = str(channel[1])
            id = str(channel[0])
            data[id] = name
        json_string = json.dumps(str(data))
        self.close_connection()
        return json_string

    def get_users(self):
        self.open_connection()
        # users_list is a list of tuples returned by a mysql.cursor.fetchall()
        users_list = self.read_all_users()
        data = {}
        for user in users_list:
            name = str(user[1])
            password = str(user[2])
            data[name] = password
        self.close_connection()
        return data

    def get_usernames(self):
        users_list = self.read_all_users()
        data = []
        for user in users_list:
            name = str(user[1])
            data.append = name
        self.close_connection()
        return data

    def create_user_if_not_exists(self, username, password, gpg):
        users = self.get_users()
        self.open_connection()
        if username not in users:
            self.create_user(username, password, gpg, 1)
        else:
            print(f"ERROR: COULDN'T CREATE USER: {username} WITH PASSWORD: {password} -- USERNAME ALREADY IN DATABASE")
        self.close_connection()

    def save_message(self, username, message, channel_id):
        self.open_connection()
        if self.get_user_permission_level(username) >= self.get_channel_permissions_level(channel_id):
            self.create_message(channel_id,
                                f"{datetime.date.today().strftime('%Y/%m/%d')} - {username} - {message}", "2025-10-10")
        self.close_connection()

    def create_channel_command(self, channel_name, channel_perm, username):
        self.open_connection()
        if int(self.get_user_permission_level(username)) > 4:
            id = int(self.count_channel()) + 1
            self.create_channel(id, channel_name, channel_perm)
            self.create_message(id, '2024/03/04 - SYSTEM - CREATED CHANNEL Lounge', '2055-05-05')
            self.close_connection()

    def upgrade_user_permissions(self, username):
        self.open_connection()
        self.upgrade_permissions(username)
        self.close_connection()