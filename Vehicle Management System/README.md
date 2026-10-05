# Vehicle Rental & Management System (VMS)
> Tool: Python 3.10+, SQLite3.
> Database: SQLite relational database (`vehicle_rental.db`) managing customers, vehicle inventory, booking transactions, and rental logs.
> Skills: Python OOP, Modular Architecture, CRUD Operations, SQLite Relational Database Management, Foreign Key Constraints.

---

### Project overview:
The Vehicle Management & Rental System (VMS) is a complete command-line interface (CLI) software built in Python backed by an SQLite relational database. It is engineered with clear role separation between standard Customers and administrative Staff (Admins), simulating real-world automobile rental workflows like Hertz or Enterprise. 

Instead of keeping static in-memory lists, the system uses persistent database storage with transactional queries. Customers can view real-time fleet availability, filter by vehicle type/brand, book rentals with automatic fare calculations based on rental days, return active vehicles, and view rental histories. Admins have dedicated elevated privileges to manage the fleet (add, update rates, remove vehicles), view all transactions, manage customer profiles, and monitor revenue analytics.

---

### Steps for building this system chronologically:

**Step 1.** Database Schema Design & Architecture:
- Designed relational tables in SQLite (`vehicle_rental.db`):
  1. `customers` table: `customer_id` (Primary Key), `name`, `email`, `phone`, `license_number`, `password`.
  2. `vehicles` table: `vehicle_id` (Primary Key), `make`, `model`, `year`, `vehicle_type` (Car, SUV, Bike, Truck), `daily_rate`, `status` (`Available` vs `Rented`).
  3. `rentals` table: `rental_id` (Primary Key), `customer_id` (Foreign Key), `vehicle_id` (Foreign Key), `rental_date`, `return_date`, `total_amount`, `status` (`Active` vs `Completed`).
- Added foreign key enforcement (`PRAGMA foreign_keys = ON;`) to prevent orphan booking records when vehicles or users are modified.

**Step 2.** Database Configuration & Abstraction Layer (`database_config.py` & `database_ops.py`):
- Created database connection handling functions with context-safe cursor operations.
- Built reusable modular database operations:
  - `add_vehicle()`, `get_all_vehicles()`, `get_available_vehicles()`, `update_vehicle_status()`, `delete_vehicle()`.
  - `register_customer()`, `authenticate_customer()`, `get_customer_by_id()`.
  - `create_rental_record()`, `process_vehicle_return()`, `get_rental_history_by_user()`, `get_all_active_rentals()`.
- Implemented error handling (`sqlite3.Error`, `try...except...finally`) to rollback failed database transactions and prevent database lock issues.

**Step 3.** Role-Based Modules (`src/customer.py` & `src/admin.py`):
- `customer.py`:
  - Customer registration and secure login validation.
  - Interactive vehicle browsing menu filtered by category, price range, and real-time availability.
  - Rental booking engine: inputs rental duration (days), calculates `total_fare = days * daily_rate`, updates vehicle availability status from `Available` to `Rented`, and issues a rental receipt.
  - Vehicle return module: updates return date timestamp, marks rental record as `Completed`, and restores vehicle status back to `Available`.
  - Rental history viewer showing active and completed bookings.

- `admin.py`:
  - Fleet management dashboard: add new vehicles with daily rental costs, edit daily rental pricing, remove decommissioned vehicles.
  - Master audit logs: view all global rental transactions, see currently rented vehicles, overdue status, and customer details.
  - Revenue analytics: calculate total fleet revenue generated from completed rentals.

**Step 4.** CLI Interface  (`main.py`):
- Designed an interactive main menu routing users cleanly into either Customer Portal or Admin Dashboard with clear session logout flows.

---

Key Features & Operations Demonstrated:
- Role-Based Access Control: Clean functional separation between end customers and fleet administrators.
- Real-Time Fleet State Management: Automatic status synchronization between `vehicles` table and `rentals` transactions upon checkout and return.
- Dynamic Fare Engine: Accurately calculates rental bills based on daily tiered rates and rental duration.
- Relational Data Integrity: Enforced primary/foreign key relationships between customers, fleet inventory, and rental receipts.
- Formatted CLI Experience: Color-coded operational prompts, tabular displays for vehicle listings, and clean exception handling.

---

Python & Database Skills Demonstrated:
- Python: Modular project structuring, OOP concepts, functional programming, exception handling, data sanitization.
- SQLite: Table DDL, relational constraints, parameterized SQL queries (`?` placeholders to prevent SQL injection), Aggregate functions (`SUM`, `COUNT`, `AVG`), multi-table `JOIN` operations.
- System Design: Separation of concerns (Business Logic / Database access layer), state preservation across app lifecycles.

---

Project Structure:
```text

 Vehicle Management System/
    ├── main.py                       # Modular runner for standalone VMS module
    └── src/
        ├── admin.py                  # Administrative handlers
        ├── customer.py               # Customer operations
        └── db/
            ├── database_config.py    # DB setup
            └── database_ops.py       # SQL logic
```

---