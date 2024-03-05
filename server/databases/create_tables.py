import mysql.connector
import credentials


cnx = mysql.connector.connect(
    host="localhost",
    user=credentials.database_username,
    password=credentials.database_password,
    database="asfaliord"
)
cursor = cnx.cursor()

# DATE in SQL is in the format YYYY-MM-DD
messages_query = ("CREATE TABLE messages ("
                  "id INT NOT NULL AUTO_INCREMENT,"
                  "content TEXT DEFAULT '',"
                  "channel_id INT NOT NULL,"
                  "time_to_live DATE,"
                  "PRIMARY KEY (id)"
                  ")")

channel_query = ("CREATE TABLE channels ("
                 "id INT NOT NULL AUTO_INCREMENT, "
                 "name TEXT DEFAULT '', "
                 "perm_lvl INT NOT NULL DEFAULT 1, "
                 "PRIMARY KEY (id)"
                 ")")

users_query = ("CREATE TABLE users ("
               "id INT NOT NULL AUTO_INCREMENT,"
               "username VARCHAR(25) NOT NULL,"
               "password VARCHAR(255) NOT NULL,"
               "public_gpg VARCHAR(500),"
               "PRIMARY KEY (id)"
               ")")

cursor.execute(messages_query)
cursor.execute(channel_query)
cursor.execute(users_query)

first_channel = ("INSERT INTO channels (name, perm_lvl) VALUES ('General', 1)")
first_message = (f"INSERT INTO messages (content, channel_id, time_to_live) VALUES ('AUTOMATED - SYSTEM - Created channel General', 1, '2055-03-03'")

cursor.execute(first_channel)
cursor.execute(first_message)

cnx.commit()
