import requests
import logging
import sqlite3

def get_uuid(username) -> str:
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT uuid FROM users WHERE ign = ?", (username.lower(),))
            uuid = cursor.fetchone()

            if uuid:
                return uuid[0]

            uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()['id']
            logging.debug(f"[GET] https://api.mojang.com/users/profiles/minecraft/")

            cursor.execute("SELECT ign FROM users WHERE uuid = ?", (uuid,))
            user_check = cursor.fetchone()

            if user_check is not None:
                cursor.execute("UPDATE users SET ign = ? WHERE uuid = ?", (username, uuid))
            else:
                cursor.execute("INSERT INTO users (uuid, ign) VALUES (?, ?)", (uuid, username.lower()))
            connection.commit()
            return uuid
    except Exception as e:
        logging.error(e)
