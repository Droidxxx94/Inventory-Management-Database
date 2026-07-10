import psycopg2

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="inventory_db",
            user="u0_a123",
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
            record_stock_movement()
        elif choice == "6":
            show_stock_history()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
if __name__ == "__main__":
    menu()
