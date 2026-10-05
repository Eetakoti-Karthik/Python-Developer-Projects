# src/admin.py
from  db.database_ops import add_vehicle, get_all_vehicles


class Admin:
    def __init__(self, vehicles):
        self.vehicles = vehicles

    def add_vehicle(self, vehicle_id, vehicle_type, brand, rent_price):
        self.vehicles[vehicle_id] = {
            "type": vehicle_type,
            "brand": brand,
            "rent_price": rent_price,
            "available": True
        }
        print(f"✅ Vehicle {brand} ({vehicle_type}) is added successfully!")

    def view_vehicles(self):
        if not self.vehicles:
                    print("No vehicles found in the database.")
                    return
        print("\n--- Vehicle List (Admin View) ---")
        for vid, details in self.vehicles.items():
            status = "Available" if details["available"] else "Rented"
            print(f"ID: {vid}, Type: {details['type']}, Brand: {details['brand']}, Rent: {details['rent_price']}, Status: {status}")
