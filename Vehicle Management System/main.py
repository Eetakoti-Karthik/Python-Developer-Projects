# main.py
from src.admin import Admin
from src.customer import Customer
from src.db.database_ops import init_db


def main():
    init_db()
    print("Database initialized successfully!")
    
    vehicles = {}
    customers = {}

    admin = Admin(vehicles)
    customer = Customer(customers, vehicles)

    while True:
        print("\n==== Welcome to Vehicle Rental System ====")
        print("1. Admin Panel")
        print("2. Customer Panel")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                print("\n--- Admin Panel ---")
                print("1. Add a Vehicle")
                print("2. View Vehicles")
                print("3. Back")
                admin_choice = input("Enter your choice: ")

                if admin_choice == "1":
                    vid = input("Enter the Vehicle ID: ")
                    vtype = input("Enter the Vehicle Type (Car/Bike/etc): ")
                    brand = input("Enter the Brand of the Vehicle: ")
                    rent = float(input("Enter Rent Price of the Vehicle: "))
                    admin.add_vehicle(vid, vtype, brand, rent)

                elif admin_choice == "2":
                    admin.view_vehicles()

                elif admin_choice == "3":
                    break

        elif choice == "2":
            while True:
                print("\n--- Customer Panel ---")
                print("1. Add a Customer")
                print("2. View the Available Vehicles")
                print("3. Rent a Vehicle")
                print("4. Return the Vehicle")
                print("5. Back")
                cust_choice = input("Enter your choice: ")

                if cust_choice == "1":
                    cid = input("Enter the Customer ID: ")
                    name = input("Enter the Customer Name: ")
                    customer.add_customer(cid, name)

                elif cust_choice == "2":
                    customer.view_available_vehicles()

                elif cust_choice == "3":
                    cid = input("Enter the Customer ID: ")
                    vid = input("Enter the Vehicle ID: ")
                    customer.rent_vehicle(cid, vid)

                elif cust_choice == "4":
                    cid = input("Enter the Customer ID: ")
                    customer.return_vehicle(cid)

                elif cust_choice == "5":
                    break

        elif choice == "3":
            print("👋 Exiting the system. Goodbye!")
            break

        else:
            print("❌ Invalid choice, please try again.")

if __name__ == "__main__":
    main()
