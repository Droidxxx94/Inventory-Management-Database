import psycopg2

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="inventory_db",
            user="myadmin",
            password="",
            host="localhost"
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

def show_products():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, unit_price FROM products;")
        rows = cur.fetchall()
        print("\n=== Product List ===")
        for row in rows:
            print(f"{row[0]} | {row[1]} | ${row[2]}")
        cur.close()
        conn.close()

def get_connection():
    return psycopg2.connect(
        dbname="inventory_db",
        user="myadmin",
        password="yourpassword",
        host="localhost",
        port="5432"
    )

def add_product():
    name = input("Enter product name: ")
    quantity = int(input("Enter quantity: "))
    unit_price = float(input("Enter unit price: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO products (name, quantity, unit_price) VALUES (%s, %s, %s)",
        (name, quantity, unit_price)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Product added successfully!")
def record_stock_movement(conn):
    product_id = int(input("Enter product ID: "))
    change_amount = int(input("Enter change amount (+/-): "))
    reason = input("Enter reason for change: ")

    update_stock(conn, product_id, change_amount)
    log_transaction(conn, product_id, change_amount, reason)

    print("Stock movement recorded.")
def log_transaction(conn, product_id, change_amount, reason):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (product_id, change_amount, reason)
        VALUES (%s, %s, %s)
    """, (product_id, change_amount, reason))
    conn.commit()


def update_stock(conn, product_id, change_amount):
    cursor = conn.cursor()

    # Update stock
    cursor.execute("""
        UPDATE products
        SET quantity = quantity + ?
        WHERE id = ?
    """, (change_amount, product_id))
    conn.commit()

    # Log the transaction
    log_transaction(conn, product_id, change_amount, "Stock update")


def view_transactions(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, p.name, t.change_amount, t.reason, t.timestamp
        FROM transactions t
        JOIN products p ON t.product_id = p.id
        ORDER BY t.timestamp DESC
    """)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def menu():
    while True:
        print("\n=== Inventory Menu ===")
        print("1. View Products")
        print("2. Add Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Record Stock Movement")
        print("6. View Stock History")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            show_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            conn = connect_db()
            if  conn:
                 record_stock_movement(conn)
                 conn.close()
        elif choice == "6":
            conn = connect_db()
            if conn:
                view_transactions(conn)
                conn.close()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
if __name__ == "__main__":
    menu()
