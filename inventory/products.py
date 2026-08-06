# products.py

import sqlite3
from inventory2.utils import (
    RED, YELLOW, GREEN, RESET,
    CRITICAL_ICON, WARNING_ICON, GOOD_ICON,
    LOW_STOCK_THRESHOLD
)
from inventory2.categories import choose_category
from inventory2.suppliers import choose_supplier


# ---------------------------------------------------------
# View all products
# ---------------------------------------------------------
def view_products(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT products.id, products.name, products.quantity, products.unit_price,
               suppliers.name, categories.name
        FROM products
        LEFT JOIN suppliers ON products.supplier_id = suppliers.id
        LEFT JOIN categories ON products.category_id = categories.id
        ORDER BY products.id
    """)

    rows = cur.fetchall()

    if not rows:
        print("No products found.")
        return

    print("\n=== Product List ===")
    for row in rows:
        qty = row[2]

        # Color logic
        if qty == 0:
            icon = CRITICAL_ICON
        elif qty < LOW_STOCK_THRESHOLD:
            icon = WARNING_ICON
        else:
            icon = GOOD_ICON

        print(f"{icon} ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Quantity: {row[2]}")
        print(f"Unit Price: ${row[3]:.2f}")
        print(f"Supplier: {row[4]}")
        print(f"Category: {row[5]}{RESET}")
        print("------------------------")


# ---------------------------------------------------------
# Add a new product
# ---------------------------------------------------------
def add_product(conn):
    cur = conn.cursor()
    try:
        name = input("Product name: ")
        quantity = int(input("Quantity: "))
        unit_price = float(input("Unit price: "))

        print("\nAssign a category:")
        category_id = choose_category(conn)

        print("\nAssign a supplier:")
        supplier_id = choose_supplier(conn)

        cur.execute("""
            INSERT INTO products (name, quantity, unit_price, supplier_id, category_id)
            VALUES (?, ?, ?, ?, ?)
        """, (name, quantity, unit_price, supplier_id, category_id))

        conn.commit()
        print("Product added successfully.")

    except Exception as e:
        print("Error adding product:", e)


# ---------------------------------------------------------
# Edit an existing product
# ---------------------------------------------------------
def edit_product(conn):
    cur = conn.cursor()
    try:
        product_id = input("Enter Product ID to edit: ")

        cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cur.fetchone()

        if not product:
            print("Product not found.")
            return

        print(f"Current Name: {product[1]}")
        new_name = input("New name (leave blank to keep current): ") or product[1]

        print(f"Current Quantity: {product[2]}")
        new_quantity = input("New quantity (leave blank to keep current): ")
        new_quantity = int(new_quantity) if new_quantity else product[2]

        print(f"Current Unit Price: {product[3]}")
        new_price = input("New price (leave blank to keep current): ")
        new_price = float(new_price) if new_price else product[3]

        change_cat = input("Change category? (y/n): ").lower()
        new_category_id = choose_category(conn) if change_cat == "y" else product[5]

        change_sup = input("Change supplier? (y/n): ").lower()
        new_supplier_id = choose_supplier(conn) if change_sup == "y" else product[4]

        cur.execute("""
            UPDATE products
            SET name = ?, quantity = ?, unit_price = ?, supplier_id = ?, category_id = ?
            WHERE id = ?
        """, (new_name, new_quantity, new_price, new_supplier_id, new_category_id, product_id))

        conn.commit()
        print("Product updated successfully.")

    except Exception as e:
        print("Error editing product:", e)


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
# Restock product
# ---------------------------------------------------------
def restock_product(conn, product_id, amount):
    cur = conn.cursor()

    cur.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
    row = cur.fetchone()

    if not row:
        return False

    new_quantity = row[0] + amount

    cur.execute("""
        UPDATE products
        SET quantity = ?
        WHERE id = ?
    """, (new_quantity, product_id))

    conn.commit()
    return True


# ---------------------------------------------------------
# Reduce stock
# ---------------------------------------------------------
def reduce_stock(conn, product_id, amount):
    cur = conn.cursor()

    cur.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
    row = cur.fetchone()

    if not row:
        return False

    current_quantity = row[0]

    if amount > current_quantity:
        return "not_enough"

    new_quantity = current_quantity - amount

    cur.execute("""
        UPDATE products
        SET quantity = ?
        WHERE id = ?
    """, (new_quantity, product_id))

    conn.commit()
    return True


# ---------------------------------------------------------
# Low-stock helper
# ---------------------------------------------------------
def get_low_stock_products(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, quantity FROM products WHERE quantity <= ?", (LOW_STOCK_THRESHOLD,))
    return cur.fetchall()
