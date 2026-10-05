import sqlite3
from typing import Optional
from database import Database

class User:
    def __init__(self, name: str, email: str, user_id: Optional[int] = None):
        self.user_id = user_id
        self.name = name
        self.email = email.strip().lower()

    def register_user(self) -> bool:
        query = "INSERT INTO Users (name, email) VALUES (?, ?);"
        try:
            self.user_id = Database.execute_write(query, (self.name, self.email))
            return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def get_user_by_email(email: str) -> Optional["User"]:
        query = "SELECT user_id, name, email FROM Users WHERE email = ?;"
        row = Database.execute_read_one(query, (email.strip().lower(),))
        if row:
            return User(user_id=row[0], name=row[1], email=row[2])
        return None