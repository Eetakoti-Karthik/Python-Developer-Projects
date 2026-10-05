import sqlite3
from typing import Any, List, Optional, Tuple

DB_PATH = "movie_booking.db"

class Database:
    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    @classmethod
    def initialize_tables(cls):
        """Creates the required tables if they do not exist."""
        create_movies = """
        CREATE TABLE IF NOT EXISTS Movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT,
            show_time TEXT NOT NULL,
            available_seats INTEGER NOT NULL
        );
        """
        create_users = """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
        """
        create_bookings = """
        CREATE TABLE IF NOT EXISTS Bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_id INTEGER NOT NULL,
            seats_booked INTEGER NOT NULL,
            booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE
        );
        """
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(create_movies)
            cursor.execute(create_users)
            cursor.execute(create_bookings)
            conn.commit()

    @classmethod
    def execute_write(cls, query: str, params: Tuple = ()) -> int:
        """Executes INSERT, UPDATE, DELETE queries and returns the last row ID."""
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

    @classmethod
    def execute_read_all(cls, query: str, params: Tuple = ()) -> List[Tuple[Any, ...]]:
        """Executes a SELECT query returning all rows."""
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    @classmethod
    def execute_read_one(cls, query: str, params: Tuple = ()) -> Optional[Tuple[Any, ...]]:
        """Executes a SELECT query returning a single row."""
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()