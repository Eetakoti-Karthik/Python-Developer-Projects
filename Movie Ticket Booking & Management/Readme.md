Movie Ticket Booking System CLI (Python, SQLite, OOP)- Console Application project.
> Language & DB: Python 3, SQLite3
> Focus: OOP principles, CRUD database operations, foreign keys, transaction handling.
---

Why Movie Ticket Booking project?
I wanted to build a practical console application to practice Python OOP and relational database concepts instead of just doing standalone script exercises. A ticket booking flow has real-world logic that needs careful handling — like preventing overbooking when seats are low, updating available seats automatically when a user books or cancels, and linking multiple tables together. I chose SQLite3 because it works out of the box with Python using the built-in `sqlite3` module and doesn't require any heavy database server setup.
---

Tables in the database (movie_booking.db):
 Table & Columns - Description 
*************************
1. Movies
   - movie_id: Integer, Primary Key, Auto-increment
   - title: Text, Title of the movie
   - genre: Text, Genre like Sci-Fi, Action, etc
   - show_time: Text, Scheduled timing of the show
   - available_seats: Integer, Total seats currently open for booking

2. Users
   - user_id: Integer, Primary Key, Auto-increment
   - name: Text, Name of the user
   - email: Text, Unique email address used for login/identification

3. Bookings
   - booking_id: Integer, Primary Key, Auto-increment
   - user_id: Integer, Foreign Key linked to Users(user_id)
   - movie_id: Integer, Foreign Key linked to Movies(movie_id)
   - seats_booked: Integer, Count of tickets booked
   - booking_time: Timestamp, Default current timestamp when ticket is booked
---

Folder and Code Structure:
  `movie_ticket_booking/`
  ├── `main.py` -> Entry point that runs the interactive CLI menu loop
  ├── `src/`
  │   ├── `__init__.py` -> Package initializer
  │   ├── `database.py` -> Connection handling, table creation, and execute helper methods
  │   ├── `admin.py` -> Movie class containing admin CRUD actions (add, update, delete, view)
  │   ├── `user.py` -> User class for user registration and fetching by email[cite: 1, 2]
  │   └── `bookings.py` -> Booking class handling ticket reservation, cancellation, and seat sync[cite: 1, 2]
  └── `db/`
      └── `movie_booking.db` -> SQLite database file

---

How the Logic Works:

1. Database & Table Setup:
   - When running `main.py`, it automatically calls `Database.initialize_tables()`.
   - Enabled `PRAGMA foreign_keys = ON;` in SQLite connection so foreign key constraints actually work properly.
   - Used parameterized queries (`?` placeholders) everywhere to prevent SQL injection errors.

2. User Registration & Session:
   - The user registers with Name and Email.
   - Email is marked as `UNIQUE`, so duplicate emails are caught via `sqlite3.IntegrityError` without crashing the program.
   - User can log in with their email, and the session tracks the active user so they don't have to keep retyping their ID for booking or cancellations.

3. Overbooking Prevention & Ticket Booking:
   - Before inserting a booking record, it queries the `Movies` table for `available_seats`.
   - If `requested_seats > available_seats`, it immediately rejects the booking and displays the remaining seat count.
   - If valid, it runs both actions inside a single transaction:
     `available_seats = available_seats - seats_booked` in `Movies`, and
     `INSERT INTO Bookings`.

4. Booking Cancellation:
   - Takes `booking_id` and checks if it actually belongs to the logged-in user.
   - Reads the booked seats, deletes the row from `Bookings`, and adds the seats back to `available_seats` in `Movies`.

5. View Bookings (SQL JOIN):
   - Uses `INNER JOIN` across `Bookings` and `Movies` on `movie_id` to display the movie title and show time alongside booking details instead of just raw IDs.

---