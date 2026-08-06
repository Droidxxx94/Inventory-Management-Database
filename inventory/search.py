# search.py

import sqlite3
from inventory2.utils import (
    RED, YELLOW, GREEN, RESET,
    LOW_STOCK_THRESHOLD
)


# ---------------------------------------------------------
# Search by Name or ID
# ---------------------------------------------------------
def search_products(conn, keyword):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, quantity, unit_price
        FROM products
        WHERE name LIKE ? OR id LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))
    return cur.fetchall()


# ---------------------------------------------------------
# Search by Category ID
# ---------------------------------------------------------
def search_products_by_category(conn):
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM categories")
    categories = cur.fetchall()

    if not categories:
        print("No categories found.")
        return

    print("\n=== Categories ===")
    for cat in categories:
        print(f"{cat[0]}. {cat[1]}")

    try:
        category_id = int(input("Enter Category ID: "))
    except ValueError:
        print("Invalid input.")
        return

    cur.execute("""
        SELECT products.id, products.name, products.quantity, products.unit_price,
               suppliers.name, categories.name
        FROM products
        LEFT JOIN suppliers ON products.supplier_id = suppliers.id
        LEFT JOIN categories ON products.category_id = categories.id
        WHERE products.category_id = ?
    """, (category_id,))

    rows = cur.fetchall()

    if not rows:
        print("No products found in this category.")
        return

    print("\n=== Products in Category ===")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Quantity: {row[2]}")
        print(f"Unit Price: ${row[3]:.2f}")
        print(f"Supplier: {row[4]}")
        print(f"Category: {row[5]}")
        print("------------------------")


# ---------------------------------------------------------
# Search by Supplier
# ---------------------------------------------------------
def search_products_by_supplier(conn):
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM suppliers")
    suppliers = cur.fetchall()

    if not suppliers:
        print("No suppliers found.")
        return

    print("\n=== Suppliers ===")
    for sup in suppliers:
        print(f"{sup[0]}. {sup[1]}")

    try:
        supplier_id = int(input("Enter Supplier ID: "))
    except ValueError:
        print("Invalid input.")
        return

    cur.execute("""
        SELECT products.id, products.name, products.quantity, products.unit_price,
               suppliers.name, categories.name
        FROM products
        LEFT JOIN suppliers ON products.supplier_id = suppliers.id
        LEFT JOIN categories ON products.category_id = categories.id
        WHERE products.supplier_id = ?
    """, (supplier_id,))

    rows = cur.fetchall()

    if not rows:
        print("No products found for this supplier.")
        return

    print("\n=== Products from Supplier ===")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Quantity: {row[2]}")
        print(f"Unit Price: ${row[3]:.2f}")
        print(f"Supplier: {row[4]}")
        print(f"Category: {row[5]}")
        print("------------------------")


# ---------------------------------------------------------
# Search by Price Range
# ---------------------------------------------------------
def search_products_by_price_range(conn):
    cur = conn.cursor()

    print("\n=== Search by Price Range ===")

    try:
        min_price = float(input("Minimum price: "))
        max_price = float(input("Maximum price: "))
    except ValueError:
        print("Invalid input. Please enter numbers.")
        return

    cur.execute("""
        SELECT products.id, products.name, products.quantity, products.unit_price,
               suppliers.name, categories.name
        FROM products
        LEFT JOIN suppliers ON products.supplier_id = suppliers.id
        LEFT JOIN categories ON products.category_id = categories.id
        WHERE products.unit_price BETWEEN ? AND ?
        ORDER BY products.unit_price ASC
    """, (min_price, max_price))

    rows = cur.fetchall()

    if not rows:
        print("No products found in this price range.")
        return

    print(f"\n=== Products priced between ${min_price} and ${max_price} ===")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Quantity: {row[2]}")
        print(f"Unit Price: ${row[3]:.2f}")
        print(f"Supplier: {row[4]}")
        print(f"Category: {row[5]}")
        print("------------------------")


# ---------------------------------------------------------
# Search Low-Stock Products
# ---------------------------------------------------------
def search_low_stock_products(conn):
    cur = conn.cursor()

    try:
        threshold = int(input("Enter low-stock threshold (e.g., 5): "))
    except ValueError:
        print("Invalid number.")
        return

    cur.execute("""
        SELECT products.id, products.name, products.quantity, products.unit_price,
               suppliers.name, categories.name
        FROM products
        LEFT JOIN suppliers ON products.supplier_id = suppliers.id
        LEFT JOIN categories ON products.category_id = categories.id
        WHERE products.quantity <= ?
        ORDER BY products.quantity ASC
    """, (threshold,))

    rows = cur.fetchall()

    if not rows:
        print("No low-stock products found.")
        return

    print(f"\n=== Products with Quantity <= {threshold} ===")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Quantity: {row[2]}")
        print(f"Unit Price: ${row[3]:.2f}")
        print(f"Supplier: {row[4]}")
        print(f"Category: {row[5]}")
        print("------------------------")


# ---------------------------------------------------------
# Search by Category Name
# ---------------------------------------------------------
def search_products_by_category_name(conn):
    cur = conn.cursor()

    keyword = input("Enter category name: ").strip()

    cur.execute("""
        SELECT id, name
        FROM categories
        WHERE name LIKE ?
    """, (f"%{keyword}%",))

    categories = cur.fetchall()

    if not categories:
        print("No categories found with that name.")
        return

    print("\n=== Matching Categories ===")
    for cat in categories:
        print(f"{cat[0]} - {cat[1]}")

    try:
        category_id = int(input("Enter the Category ID to view products: "))
    except ValueError:
        print("Invalid input.")
        return

    cur.execute("""
        SELECT products.id, products.name, products.quantity, products.unit_price,
               suppliers.name, categories.name
        FROM products
        LEFT JOIN suppliers ON products.supplier_id = suppliers.id
        LEFT JOIN categories ON products.category_id = categories.id
        WHERE products.category_id = ?
    """, (category_id,))

    rows = cur.fetchall()

    if not rows:
        print("No products found in this category.")
        return

    print(f"\n=== Products in Category '{keyword}' ===")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Quantity: {row[2]}")
        print(f"Unit Price: ${row[3]:.2f}")
        print(f"Supplier: {row[4]}")
        print(f"Category: {row[5]}")
        print("------------------------")


# ---------------------------------------------------------
# Search by Inventory Value (qty × price)
# ---------------------------------------------------------
def search_products_by_inventory_value(conn):
    cur = conn.cursor()

    print("\n=== Search by Inventory Value (Quantity × Price) ===")

    try:
        min_value = float(input("Minimum inventory value: "))
        max_value = float(input("Maximum inventory value: "))
    except ValueError:
        print("Invalid input. Please enter numbers.")
        return

    cur.execute("""
        SELECT products.id, products.name, products.quantity, products.unit_price,
               (products.quantity * products.unit_price) AS inventory_value,
               suppliers.name, categories.name
        FROM products
        LEFT JOIN suppliers ON products.supplier_id = suppliers.id
        LEFT JOIN categories ON products.category_id = categories.id
        WHERE inventory_value BETWEEN ? AND ?
        ORDER BY inventory_value DESC
    """, (min_value, max_value))

    rows = cur.fetchall()

    if not rows:
        print("No products found in this inventory value range.")
        return

    print(f"\n=== Products with Inventory Value between ${min_value} and ${max_value} ===")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Quantity: {row[2]}")
        print(f"Unit Price: ${row[3]:.2f}")
        print(f"Inventory Value: ${row[4]:.2f}")
        print(f"Supplier: {row[5]}")
        print(f"Category: {row[6]}")
        print("------------------------")
