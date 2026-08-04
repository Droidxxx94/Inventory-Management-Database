
import sqlite3

def connect_db():
    try:
        conn = sqlite3.connect('inventory.db')
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

def create_tables(conn):
    cur = conn.cursor()

    # Products table (already exists)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            supplier_id INTEGER,
            category_id INTEGER,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    # Suppliers table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT
        )
    """)

    # Categories table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    # Transactions table (already exists)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            change_amount INTEGER,
            reason TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()        

