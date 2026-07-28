import sqlite3
from inventory.db import connect_db

# ---------------------------------------------------------
# Add timestamp column if missing
# ---------------------------------------------------------
def add_timestamp_column():
    conn = connect_db()
    if conn:
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
        finally:
            cur.close()
            conn.close()

# ---------------------------------------------------------
# Show all products
# ---------------------------------------------------------
def show_products():
    conn = connect_db()
    if not conn:
        print("Database connection failed.")
        return

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
    finally:
        cur.close()
        conn.close()

# ---------------------------------------------------------
# Add a new product
# ---------------------------------------------------------
def add_product():
    conn = connect_db()
    if not conn:
        print("Database connection failed.")
        return

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
    finally:
        cur.close()
        conn.close()

# ---------------------------------------------------------
# Update an existing product
# ---------------------------------------------------------
def update_product():
    conn = connect_db()
    if not conn:
        print("Database connection failed.")
        return

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
    finally:
        cur.close()
        conn.close()

# ---------------------------------------------------------
# Delete a product
# ---------------------------------------------------------
def delete_product():
    conn = connect_db()
    if not conn:
        print("Database connection failed.")
        return

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
    finally:
        cur.close()
        conn.close()

# ---------------------------------------------------------
# Record stock movement (transaction)
# ---------------------------------------------------------
def record_stock_movement():
    conn = connect_db()
    if not conn:
        print("Database connection failed.")
        return

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
    finally:
        cur.close()
        conn.close()

# ---------------------------------------------------------
# View all transactions
# ---------------------------------------------------------
def view_transactions():
    conn = connect_db()
    if not conn:
        print("Database connection failed.")
        return

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
    finally:
        cur.close()
        conn.close()

# ---------------------------------------------------------
# Main Menu
# ---------------------------------------------------------
def menu():
    while True:
        print("\n=== Inventory Menu ===")
        print("1. Show Products")
        print("2. Add Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Record Stock Movement")
        print("6. View Transactions")
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
            view_transactions()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# ---------------------------------------------------------
# Program Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    add_timestamp_column()
    menu()
