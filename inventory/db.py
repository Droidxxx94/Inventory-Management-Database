
import sqlite3

def connect_db():
    try:
        conn = sqlite3.connect('inventory/database/inventory.db')
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

