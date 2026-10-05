# database_ops.py
import sqlite3
from database_config import (
    DB_NAME, CREATE_VEHICLES_TABLE, CREATE_CUSTOMERS_TABLE,
    INSERT_VEHICLE, GET_ALL_VEHICLES, GET_AVAILABLE_VEHICLES,
    GET_VEHICLE_BY_ID, UPDATE_AVAILABILITY,
    INSERT_CUSTOMER, GET_CUSTOMER_BY_ID, UPDATE_CUSTOMER_RENTAL
)


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_VEHICLES_TABLE)
    cursor.execute(CREATE_CUSTOMERS_TABLE)
    conn.commit()
    conn.close()


def add_vehicle(vehicle_id, vehicle_type, brand, rent_price):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(INSERT_VEHICLE, (vehicle_id, vehicle_type, brand, rent_price))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_all_vehicles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(GET_ALL_VEHICLES)
    vehicles = cursor.fetchall()
    conn.close()
    return vehicles


def get_available_vehicles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(GET_AVAILABLE_VEHICLES)
    vehicles = cursor.fetchall()
    conn.close()
    return vehicles


def get_vehicle_by_id(vehicle_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(GET_VEHICLE_BY_ID, (vehicle_id,))
    vehicle = cursor.fetchone()
    conn.close()
    return vehicle


def update_availability(vehicle_id, available):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(UPDATE_AVAILABILITY, (1 if available else 0, vehicle_id))
    conn.commit()
    conn.close()


def add_customer(customer_id, name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(INSERT_CUSTOMER, (customer_id, name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_customer_by_id(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(GET_CUSTOMER_BY_ID, (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    return customer


def update_customer_rental(customer_id, vehicle_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(UPDATE_CUSTOMER_RENTAL, (vehicle_id, customer_id))
    conn.commit()
    conn.close()