from typing import List, Optional
from database import Database

class Movie:
    def __init__(self, title: str, genre: str, show_time: str, available_seats: int, movie_id: Optional[int] = None):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.show_time = show_time
        self.available_seats = available_seats

    def add_movie(self) -> int:
        query = """
        INSERT INTO Movies (title, genre, show_time, available_seats)
        VALUES (?, ?, ?, ?);
        """
        self.movie_id = Database.execute_write(query, (self.title, self.genre, self.show_time, self.available_seats))
        return self.movie_id

    @staticmethod
    def update_movie(movie_id: int, title: str, genre: str, show_time: str, available_seats: int) -> bool:
        query = """
        UPDATE Movies
        SET title = ?, genre = ?, show_time = ?, available_seats = ?
        WHERE movie_id = ?;
        """
        Database.execute_write(query, (title, genre, show_time, available_seats, movie_id))
        return True

    @staticmethod
    def delete_movie(movie_id: int) -> bool:
        query = "DELETE FROM Movies WHERE movie_id = ?;"
        Database.execute_write(query, (movie_id,))
        return True

    @staticmethod
    def get_movie_by_id(movie_id: int) -> Optional["Movie"]:
        query = "SELECT movie_id, title, genre, show_time, available_seats FROM Movies WHERE movie_id = ?;"
        row = Database.execute_read_one(query, (movie_id,))
        if row:
            return Movie(movie_id=row[0], title=row[1], genre=row[2], show_time=row[3], available_seats=row[4])
        return None

    @staticmethod
    def get_all_movies() -> List["Movie"]:
        query = "SELECT movie_id, title, genre, show_time, available_seats FROM Movies;"
        rows = Database.execute_read_all(query)
        return [Movie(movie_id=r[0], title=r[1], genre=r[2], show_time=r[3], available_seats=r[4]) for r in rows]