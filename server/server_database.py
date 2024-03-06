import mysql.connector
from datetime import datetime
from hashlib import sha1
from random import randint
import os
import sys
sys.path.insert(1,f'{os.getcwd()}/../..')
import credentials


class ServerDatabase:
    def __init__(self):
        self.open_connection()

    def open_connection(self):
        self.cnx = mysql.connector.connect(
            host="localhost",
            user=credentials.mariadb_user,
            password=credentials.mariadb_password,
            database="asfaliord"
        )
        self.cursor = self.cnx.cursor()

    # Simple CRUD operations for each table of the server-side database
    def create_user(self, username, password, gpg_pk, perm_lvl):
        query = "INSERT INTO users (username, password, public_gpg, perm_lvl) VALUES (%s, %s, %s, %s)"
        data = (username, password, gpg_pk, perm_lvl)
        self.cursor.execute(query, data)
        self.cnx.commit()

    def read_user(self, user_id):
        query = "SELECT * FROM users WHERE id = %s"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()

    def read_all_users(self):
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_user_permission_level(self, username):
        permissions_level = self.read_user(self.get_user_id(username))[4]
        return permissions_level

    def get_user_id(self, username):
        query = "SELECT id FROM users WHERE username = %s"
        self.cursor.execute(query, (username, ))
        return self.cursor.fetchone()[0]

    def update_user(self, user_id, column, new_value):
        data = (column, new_value, user_id)
        query = "UPDATE users SET username = %s WHERE id = %s"
        self.cursor.execute(query, data)
        self.cnx.commit()

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id = %s"
        self.cursor.execute(query, (user_id,))
        self.cnx.commit()

    # Channels CRUD operations
    def create_channel(self, id, name, min_perm_lvl):
        data = (id, name, min_perm_lvl)
        query = "INSERT INTO channels (id, name, perm_lvl) VALUES (%s, %s, %s)"
        self.cursor.execute(query, data)
        self.cnx.commit()

    def count_channel(self):
        query = "SELECT COUNT(*) FROM channels"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def read_channel(self, channel_id):
        query = "SELECT * FROM channels WHERE id = %s"
        self.cursor.execute(query, (channel_id,))
        return self.cursor.fetchone()

    def get_channel_permissions_level(self, channel_id):
        return self.read_channel(channel_id)[2]

    def read_all_channels(self, permissions_level):
        query = "SELECT * FROM channels WHERE perm_lvl <= %s"
        self.cursor.execute(query, (permissions_level,))
        return self.cursor.fetchall()

    def update_channel(self, channel_id, column, new_value):
        data = (column, new_value, channel_id)
        query = "UPDATE channels SET %s = %s WHERE id = %s"
        self.cursor.execute(query, data)
        self.cnx.commit()

    def delete_channel(self, channel_id):
        query = "DELETE FROM channels WHERE id = %s"
        self.cursor.execute(query, (channel_id,))
        self.cnx.commit()

    # Messages CRUD operations
    def create_message(self, channel_id, content, ttl):
        data = (content, channel_id, ttl)
        query = "INSERT INTO messages (content, channel_id, time_to_live) VALUES (%s, %s, %s)"
        self.cursor.execute(query, data)
        self.cnx.commit()

    def read_message(self, message_id):
        # Returns a tuple
        query = "SELECT * FROM messages WHERE id = %s"
        self.cursor.execute(query, (message_id,))
        return self.cursor.fetchone()

    def read_all_messages(self, permissions_level):
        # Returns a list of tuples
        query = (f"SELECT messages.* FROM messages INNER JOIN channels ON messages.channel_id = channels.id "
                 f"WHERE channels.perm_lvl <= {permissions_level}")
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_message(self, message_id, column, new_value):
        data = (column, new_value, message_id)
        query = "UPDATE messages SET %s = %s WHERE id = %s"
        self.cursor.execute(query, data)
        self.cnx.commit()

    def delete_message(self, message_id):
        query = "DELETE FROM messages WHERE id = %s"
        self.cursor.execute(query, (message_id,))
        self.cnx.commit()

    def count_messages(self):
        self.cursor.execute("SELECT COUNT(*) FROM messages")
        messages_count = self.cursor.fetchone()[0]
        return messages_count

    def flush_messages(self):
        messages_count = self.count_messages()
        for i in range(messages_count):
            # Creates a sha1 (fastest sha, more time-efficient relative to our needs) that replaces the hashed message
            # content. For basic opsec purposes, making it look like a real message for the human eye.
            data = (sha1(chr(randint(1, 122)).encode('utf-8')).hexdigest(), i)
            query = (f"UPDATE messages SET content = %s WHERE id = %s")
            self.cursor.execute(query, data)
            self.cnx.commit()

    def close_connection(self):
        self.cursor.close()
        self.cnx.close()