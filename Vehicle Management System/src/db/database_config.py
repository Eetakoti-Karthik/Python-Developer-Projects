# database_config.py
DB_NAME = "vehicle_rental.db"

CREATE_VEHICLES_TABLE = """
CREATE TABLE IF NOT EXISTS Vehicles (
    vehicle_id TEXT PRIMARY KEY,
    vehicle_type TEXT NOT NULL,
    brand TEXT NOT NULL,
    rent_price REAL NOT NULL,
    is_available INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_CUSTOMERS_TABLE = """
CREATE TABLE IF NOT EXISTS Customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    rented_vehicle TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERT_VEHICLE = "INSERT INTO Vehicles (vehicle_id, vehicle_type, brand, rent_price) VALUES (?, ?, ?, ?);"
GET_ALL_VEHICLES = "SELECT * FROM Vehicles;"
GET_AVAILABLE_VEHICLES = "SELECT * FROM Vehicles WHERE is_available = 1;"
GET_VEHICLE_BY_ID = "SELECT * FROM Vehicles WHERE vehicle_id = ?;"
UPDATE_AVAILABILITY = "UPDATE Vehicles SET is_available = ? WHERE vehicle_id = ?;"

INSERT_CUSTOMER = "INSERT INTO Customers (customer_id, name) VALUES (?, ?);"
GET_CUSTOMER_BY_ID = "SELECT * FROM Customers WHERE customer_id = ?;"
UPDATE_CUSTOMER_RENTAL = "UPDATE Customers SET rented_vehicle = ? WHERE customer_id = ?;"