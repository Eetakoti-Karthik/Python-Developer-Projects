import sqlite3
from typing import List, Tuple, Any, Optional
from database import Database

class Booking:
    def __init__(self, user_id: int, movie_id: int, seats_booked: int, booking_id: Optional[int] = None, booking_time: Optional[str] = None):
        self.booking_id = booking_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.seats_booked = seats_booked
        self.booking_time = booking_time

    def book_ticket(self) -> Tuple[bool, str]:
        """Atomically books tickets and decrements movie available seats."""
        conn = Database.get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT available_seats FROM Movies WHERE movie_id = ?;", (self.movie_id,))
                row = cursor.fetchone()

                if not row:
                    return False, "Movie not found."

                available = row[0]
                if available < self.seats_booked:
                    return False, f"Not enough seats available. Remaining: {available}."

                cursor.execute(
                    "UPDATE Movies SET available_seats = available_seats - ? WHERE movie_id = ?;",
                    (self.seats_booked, self.movie_id)
                )

                cursor.execute(
                    "INSERT INTO Bookings (user_id, movie_id, seats_booked) VALUES (?, ?, ?);",
                    (self.user_id, self.movie_id, self.seats_booked)
                )
                self.booking_id = cursor.lastrowid
                return True, f"Booking successful! Your Booking ID is {self.booking_id}."
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            conn.close()

    @staticmethod
    def cancel_booking(booking_id: int, user_id: int) -> Tuple[bool, str]:
        """Cancels a booking and restores seats back to the movie."""
        conn = Database.get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT movie_id, seats_booked FROM Bookings WHERE booking_id = ? AND user_id = ?;",
                    (booking_id, user_id)
                )
                booking = cursor.fetchone()
                if not booking:
                    return False, "Booking record not found or does not belong to your account."

                movie_id, seats = booking

                cursor.execute("DELETE FROM Bookings WHERE booking_id = ?;", (booking_id,))
                cursor.execute(
                    "UPDATE Movies SET available_seats = available_seats + ? WHERE movie_id = ?;",
                    (seats, movie_id)
                )
                return True, "Booking cancelled successfully. Seats have been restored."
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            conn.close()

    @staticmethod
    def view_user_bookings(user_id: int) -> List[Tuple[Any, ...]]:
        """Fetches joined booking information for a specific user."""
        query = """
        SELECT b.booking_id, m.title, m.show_time, b.seats_booked, b.booking_time
        FROM Bookings b
        JOIN Movies m ON b.movie_id = m.movie_id
        WHERE b.user_id = ?
        ORDER BY b.booking_time DESC;
        """
        return Database.execute_read_all(query, (user_id,))