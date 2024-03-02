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
messages_query = ("CREATE TABLE 'messages' ("
                  "'id' INT NOT NULL AUTO_INCREMENT,"
                  "'content' TEXT DEFAULT '',"
                  "'channel_id' INT NOT NULL,"
                  "'time_to_live' DATE,"
                  "PRIMARY KEY ('id')"
                  ")")

channel_query = ("CREATE TABLE 'channels' ("
                 "'id' INT NOT NULL AUTO_INCREMENT, "
                 "'name' TEXT DEFAULT '', "
                 "'permissions_level' INT NOT NULL DEFAULT '1', "
                 "PRIMARY KEY (`id`)"
                 ")")

users_query = ("CREATE TABLE `channels` ("
               "`id` INT NOT NULL AUTO_INCREMENT,"
               "`username` VARCHAR(25) NOT NULL,"
               "`password` VARCHAR(255) NOT NULL,"
               "`public_gpg` VARCHAR(500),"
               "PRIMARY KEY (`id`)"
               ")")

cursor.execute(messages_query)
cursor.execute(channel_query)
cursor.execute(users_query)
cnx.commit()
