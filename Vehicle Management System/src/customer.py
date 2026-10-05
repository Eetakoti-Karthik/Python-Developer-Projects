# src/customer.py
from db.database_ops import (
    get_available_vehicles, get_vehicle_by_id,
    get_customer_by_id, update_availability,
    update_customer_rental, add_customer as db_add_customer
)
class Customer:
    def __init__(self, customers, vehicles):
        self.customers = customers
        self.vehicles = vehicles

    def add_customer(self, customer_id, name):
        self.customers[customer_id] = {
            "name": name,
            "rented_vehicle": None
        }
        print(f"✅ Customer {name} added successfully!")

    def view_available_vehicles(self):
        vehicles = get_available_vehicles()
        print("\n--- Available Vehicles ---")
        available = False
        for vid, details in self.vehicles.items():
            if details["available"]:
                print(f"ID: {vid}, Type: {details['type']}, Brand: {details['brand']}, Rent: {details['rent_price']}")
                available = True
        if not available:
            print("❌ No vehicles available.")

    def rent_vehicle(self, customer_id, vehicle_id):
         # Check customer exists
        customer = get_customer_by_id(customer_id)
        if not customer:
            print("❌ Customer does not exist!")
            return
        
        # Check customer doesn't already have a rental
        if customer[2]:  # rented_vehicle column
            print(f"Customer already has a rented vehicle: {customer[2]}")
            return
        
        # Check vehicle exists
        vehicle = get_vehicle_by_id(vehicle_id)
        if not vehicle:
            print("❌ Vehicle ID not found!")
            return

        # Check vehicle is available
        if not vehicle[4]:
            print("❌ Vehicle already rented!")
            return
        
        # Assign vehicle
        update_availability(vehicle_id, False)
        update_customer_rental(customer_id, vehicle_id)
        print(f"✅ {customer[1]} rented {vehicle[2]} ({vehicle[1]}) 🎉")
        
    def return_vehicle(self, customer_id):
        # Check customer exists
        customer = get_customer_by_id(customer_id)
        if not customer:
            print("❌ Customer does not exist!")
            return

        rented = customer[2]  
        # rented_vehicle column
        if not rented:
            print("⚠️ No vehicle rented by this customer.")
            return
        
         # Free up vehicle
        vehicle = get_vehicle_by_id(rented)
        update_availability(rented, True)
        update_customer_rental(customer_id, None)
        print(f"✅{customer[1]} returned {vehicle[2]} ({vehicle[1]}) 👍")
        