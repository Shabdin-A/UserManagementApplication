import hashlib
import sqlite3
from Common.user import User


class UserDataAccess:
    def __init__(self):
        self.database_name = "UserManagementDB04-222.db"

    def hash_password(self, password):
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    def get_user(self, username, password):
        hashed_password = self.hash_password(password)
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            data = cursor.execute(f"""
            SELECT  id,
                    first_name,
                    last_name,
                    username,
                    password,
                    active,
                    role_id
            FROM    user
            WHERE   username    =    ?
            AND     password    =    ?""", [username, hashed_password]).fetchone()

            if data:
                user = User(data[0], data[1], data[2], data[3], None, data[5], data[6])
                return user

    def get_users(self, user_id):
        user_list = []
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            data = cursor.execute(f"""
            SELECT  id,
                    first_name,
                    last_name,
                    username,
                    password,
                    active,
                    role_id
            FROM    user
            WHERE   id  !=  ?""", [user_id]).fetchall()

            for item in data:
                user = User(item[0], item[1], item[2], item[3], None, item[5], item[6])
                user_list.append(user)

            return user_list

    def update_active(self, user_id, new_active):
        user_list = []
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""
            Update  User
            set     active =    ?
            Where   id     =    ?""", [new_active, user_id])

            connection.commit()

    def new_user(self, first_name, last_name, username, password):
        hashed_password = self.hash_password(password)
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO user (
                    first_name,
                    last_name,
                    username,
                    password
                )
                VALUES (?, ?, ?, ?);
            """, [first_name, last_name, username, hashed_password])
            connection.commit()

    def get_user_by_username(self, username):
        with sqlite3.connect(self.database_name) as connection:
            curses = connection.cursor()
            curses.execute("""
            SELECT *
            FROM user
            WHERE username = ?""", [username])
            return curses.fetchone()

    def change_role_id(self, user_id, role_id):
        with sqlite3.connect(self.database_name) as connection:
            curses = connection.cursor()
            curses.execute(f"""
            UPDATE user
            SET role_id =    ?
            WHERE id    =    ?""", [role_id, user_id])
            connection.commit()

    def get_user_info(self, user_id):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            user = cursor.execute("""
                SELECT  id,
                        first_name,
                        last_name,
                        username, 
                        password
                FROM    user
                WHERE   id = ?""", [user_id]).fetchone()
            if user:
                return {"id": user[0], "first_name": user[1], "last_name": user[2], "username": user[3],
                        "password": user[4]}
            return None

    def update_user_info(self, user_id, first_name, last_name, username, password):
        hashed_password = self.hash_password(password)
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE user
                SET     first_name = ?, 
                        last_name = ?, 
                        username = ?, 
                        password = ?
                WHERE   id = ?
            """, [first_name, last_name, username, hashed_password, user_id])
            connection.commit()
            return cursor.rowcount > 0

    def check_current_password(self, user_id, current_password):
        hashed_password = self.hash_password(current_password)
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT password
                FROM user
                WHERE id = ?
            """, [user_id])
            stored_password = cursor.fetchone()
            return stored_password and stored_password[0] == hashed_password

    def update_password(self, user_id, new_password):
        hashed_password = self.hash_password(new_password)
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE user
                SET password = ?
                WHERE id = ?
            """, [hashed_password, user_id])
            connection.commit()
            return cursor.rowcount > 0

