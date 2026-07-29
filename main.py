import sqlite3
from inventory.db import connect_db
from inventory.reports import (
    get_inventory_value,
    get_low_stock_items,
    get_supplier_counts,
    get_category_summary,
    get_top_value_products
)

# ---------------------------------------------------------
# Add timestamp column if missing
# ---------------------------------------------------------
def add_timestamp_column(conn):
    cur = conn.cursor()
    try:
        cur.execute("""
            ALTER TABLE transactions
            ADD COLUMN timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        """)
        conn.commit()
        print("Timestamp column added.")
    except sqlite3.OperationalError:
        # Column already exists
        pass

# ---------------------------------------------------------
# Show all products
# ---------------------------------------------------------
def show_products(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()

        print("\n=== Product List ===")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Qty: {row[2]}, Price: ${row[3]}")
        print()
    except Exception as e:
        print("Error showing products:", e)

# ---------------------------------------------------------
# Add a new product
# ---------------------------------------------------------
def add_product(conn):
    cur = conn.cursor()
    try:
        name = input("Product name: ")
        quantity = int(input("Quantity: "))
        price = float(input("Unit price: "))

        cur.execute("""
            INSERT INTO products (name, quantity, unit_price)
            VALUES (?, ?, ?)
        """, (name, quantity, price))

        conn.commit()
        print("Product added successfully.")
    except Exception as e:
        print("Error adding product:", e)

# ---------------------------------------------------------
# Update an existing product
# ---------------------------------------------------------
def update_product(conn):
    cur = conn.cursor()
    try:
        product_id = input("Enter product ID to update: ")

        cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cur.fetchone()

        if not product:
            print("Product not found.")
            return

        print("\nLeave blank to keep current value.\n")

        new_name = input(f"New name (current: {product[1]}): ") or product[1]
        new_quantity = input(f"New quantity (current: {product[2]}): ") or product[2]
        new_price = input(f"New price (current: {product[3]}): ") or product[3]

        cur.execute("""
            UPDATE products
            SET name = ?, quantity = ?, unit_price = ?
            WHERE id = ?
        """, (new_name, new_quantity, new_price, product_id))

        conn.commit()
        print("Product updated successfully.")
    except Exception as e:
        print("Error updating product:", e)

# ---------------------------------------------------------
# Delete a product
# ---------------------------------------------------------
def delete_product(conn):
    cur = conn.cursor()
    try:
        product_id = input("Enter product ID to delete: ")

        cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cur.fetchone()

        if not product:
            print("Product not found.")
            return

        print(f"\nAre you sure you want to delete '{product[1]}'?")
        confirm = input("Type YES to confirm: ")

        if confirm.upper() == "YES":
            cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            print("Product deleted.")
        else:
            print("Delete canceled.")
    except Exception as e:
        print("Error deleting product:", e)

# ---------------------------------------------------------
# Record stock movement (transaction)
# ---------------------------------------------------------
def record_stock_movement(conn):
    cur = conn.cursor()
    try:
        product_id = input("Product ID: ")
        change_amount = int(input("Change amount (+/-): "))
        reason = input("Reason: ")

        cur.execute("""
            INSERT INTO transactions (product_id, change_amount, reason)
            VALUES (?, ?, ?)
        """, (product_id, change_amount, reason))

        conn.commit()
        print("Stock movement recorded.")
    except Exception as e:
        print("Error recording movement:", e)

# ---------------------------------------------------------
# View all transactions
# ---------------------------------------------------------
def view_transactions(conn):
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT t.id, p.name, t.change_amount, t.reason, t.timestamp
            FROM transactions t
            LEFT JOIN products p ON t.product_id = p.id
            ORDER BY t.timestamp DESC
        """)

        rows = cur.fetchall()

        print("\n=== Transaction History ===")
        for row in rows:
            print(f"ID: {row[0]}, Product: {row[1]}, Change: {row[2]}, Reason: {row[3]}, Time: {row[4]}")
        print()
    except Exception as e:
        print("Error viewing transactions:", e)

# ---------------------------------------------------------
# Reports & Analytics Menu
# ---------------------------------------------------------
def show_reports_menu(conn):
    print("\n=== Reports & Analytics ===")
    print("1. Total Inventory Value")
    print("2. Low Stock Items")
    print("3. Supplier Summary")
    print("4. Category Summary")
    print("5. Top Value Products")
    print("0. Back")

    option = input("Choose an option: ")

    if option == "1":
        print("Total Inventory Value:", get_inventory_value(conn))

    elif option == "2":
        for item in get_low_stock_items(conn):
            print(item)

    elif option == "3":
        for row in get_supplier_counts(conn):
            print(row)

    elif option == "4":
        for row in get_category_summary(conn):
            print(row)

    elif option == "5":
        for row in get_top_value_products(conn):
            print(row)

    elif option == "0":
        return

# ---------------------------------------------------------
# Main Menu
# ---------------------------------------------------------
def main_menu(conn):
    while True:
        print("\n=== Inventory Management System ===")
        print("1. Show Products")
        print("2. Add Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Record Stock Movement")
        print("6. View Transactions")
        print("7. Print Goodbye / Exit")
        print("8. Reports & Analytics")

        choice = input("Choose an option: ")

        if choice == "1":
            show_products(conn)

        elif choice == "2":
            add_product(conn)

        elif choice == "3":
            update_product(conn)

        elif choice == "4":
            delete_product(conn)

        elif choice == "5":
            record_stock_movement(conn)

        elif choice == "6":
            view_transactions(conn)

        elif choice == "7":
            print("Goodbye!")
            break

        elif choice == "8":
            show_reports_menu(conn)

        else:
            print("Invalid option. Please try again.")

# ---------------------------------------------------------
# Program Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    conn = connect_db()
    add_timestamp_column(conn)
    main_menu(conn)