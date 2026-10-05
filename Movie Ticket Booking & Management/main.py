import sys
from src.database import Database
from src.admin import Movie
from src.user import User
from src.bookings import Booking

def seed_sample_data():
    """Seeds starter movies if none exist."""
    movies = Movie.get_all_movies()
    if not movies:
        Movie("Inception", "Sci-Fi", "18:00", 50).add_movie()
        Movie("Interstellar", "Sci-Fi", "21:00", 40).add_movie()
        Movie("The Dark Knight", "Action", "15:00", 30).add_movie()

def display_movies():
    movies = Movie.get_all_movies()
    if not movies:
        print("\nNo movies currently scheduled.")
        return
    print("\n{:<6} {:<25} {:<15} {:<12} {:<10}".format("ID", "Title", "Genre", "Time", "Seats"))
    print("-" * 72)
    for m in movies:
        print(f"{m.movie_id:<6} {m.title:<25} {m.genre:<15} {m.show_time:<12} {m.available_seats:<10}")

def register_flow():
    print("\n--- User Registration ---")
    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()
    if not name or not email:
        print("Name and email cannot be empty.")
        return
    user = User(name, email)
    if user.register_user():
        print(f"Registration successful! Welcome, {user.name} (User ID: {user.user_id}).")
    else:
        print("Registration failed: Email already registered.")

def login_flow():
    email = input("Enter your registered email: ").strip()
    user = User.get_user_by_email(email)
    if not user:
        print("User not found. Please register first.")
        return None
    print(f"\nWelcome back, {user.name}!")
    return user

def book_ticket_flow(user: User):
    display_movies()
    try:
        movie_id = int(input("\nEnter Movie ID to book: ").strip())
        seats = int(input("Enter number of seats to book: ").strip())
        if seats <= 0:
            print("Seats must be a positive number.")
            return
    except ValueError:
        print("Invalid input: Please enter valid numbers.")
        return

    booking = Booking(user_id=user.user_id, movie_id=movie_id, seats_booked=seats)
    success, message = booking.book_ticket()
    print(message)

def cancel_ticket_flow(user: User):
    try:
        booking_id = int(input("\nEnter Booking ID to cancel: ").strip())
    except ValueError:
        print("Invalid input: Booking ID must be a number.")
        return

    success, message = Booking.cancel_booking(booking_id, user.user_id)
    print(message)

def view_bookings_flow(user: User):
    bookings = Booking.view_user_bookings(user.user_id)
    if not bookings:
        print("\nYou have no active bookings.")
        return
    print("\n{:<12} {:<25} {:<12} {:<8} {:<20}".format("Booking ID", "Movie", "Time", "Seats", "Booked At"))
    print("-" * 80)
    for b in bookings:
        print(f"{b[0]:<12} {b[1]:<25} {b[2]:<12} {b[3]:<8} {b[4]:<20}")

def admin_flow():
    print("\n--- Admin Management ---")
    print("1. Add Movie")
    print("2. Update Movie")
    print("3. Delete Movie")
    print("4. View All Movies")
    choice = input("Enter choice (1-4): ").strip()

    if choice == "1":
        title = input("Title: ").strip()
        genre = input("Genre: ").strip()
        time = input("Show Time (e.g., 18:00): ").strip()
        try:
            seats = int(input("Available Seats: ").strip())
            m = Movie(title, genre, time, seats)
            m.add_movie()
            print(f"Movie added with ID {m.movie_id}!")
        except ValueError:
            print("Seats must be a valid integer.")
    elif choice == "2":
        try:
            mid = int(input("Enter Movie ID to update: ").strip())
            title = input("New Title: ").strip()
            genre = input("New Genre: ").strip()
            time = input("New Show Time: ").strip()
            seats = int(input("New Seats: ").strip())
            Movie.update_movie(mid, title, genre, time, seats)
            print("Movie updated successfully.")
        except ValueError:
            print("Invalid inputs.")
    elif choice == "3":
        try:
            mid = int(input("Enter Movie ID to delete: ").strip())
            Movie.delete_movie(mid)
            print("Movie removed.")
        except ValueError:
            print("Invalid ID.")
    elif choice == "4":
        display_movies()

def main():
    Database.initialize_tables()
    seed_sample_data()

    current_user = None

    while True:
        user_status = f"Logged in as: {current_user.name} ({current_user.email})" if current_user else "Not logged in"
        print(f"\n==============================")
        print(f" 🎬 MOVIE TICKET BOOKING SYSTEM")
        print(f" Status: {user_status}")
        print(f"==============================")
        print("1. Register User")
        print("2. Login")
        print("3. View Movies")
        print("4. Book Ticket")
        print("5. Cancel Booking")
        print("6. View My Bookings")
        print("7. Admin Panel")
        print("8. Logout")
        print("9. Exit")

        choice = input("Select an option (1-9): ").strip()

        if choice == "1":
            register_flow()
        elif choice == "2":
            user = login_flow()
            if user:
                current_user = user
        elif choice == "3":
            display_movies()
        elif choice == "4":
            if not current_user:
                print("Please log in first to book tickets.")
            else:
                book_ticket_flow(current_user)
        elif choice == "5":
            if not current_user:
                print("Please log in first to manage bookings.")
            else:
                cancel_ticket_flow(current_user)
        elif choice == "6":
            if not current_user:
                print("Please log in first to view bookings.")
            else:
                view_bookings_flow(current_user)
        elif choice == "7":
            admin_flow()
        elif choice == "8":
            current_user = None
            print("Logged out successfully.")
        elif choice == "9":
            print("Exiting application. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please choose between 1 and 9.")

if __name__ == "__main__":
    main()