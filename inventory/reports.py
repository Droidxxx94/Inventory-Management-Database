# reports.py

import sqlite3
from inventory.utils import (
    RED, YELLOW, GREEN, RESET,
    LOW_STOCK_THRESHOLD,
    CRITICAL_ICON, WARNING_ICON, GOOD_ICON
)
from inventory.products import get_low_stock_products
from inventory.db import connect_db


# ---------------------------------------------------------
# Total Inventory Value
# ---------------------------------------------------------
def get_inventory_value(conn):
    cur = conn.cursor()
    cur.execute("SELECT quantity, unit_price FROM products")
    rows = cur.fetchall()

    total = sum(qty * price for qty, price in rows)
    return total


# ---------------------------------------------------------
# Low Stock Items
# ---------------------------------------------------------
def get_low_stock_items(conn):
    return get_low_stock_products(conn)


# ---------------------------------------------------------
# Supplier Summary
# ---------------------------------------------------------
def get_supplier_counts(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT suppliers.name, COUNT(products.id)
        FROM suppliers
        LEFT JOIN products ON products.supplier_id = suppliers.id
        GROUP BY suppliers.id
    """)
    return cur.fetchall()


# ---------------------------------------------------------
# Category Summary
# ---------------------------------------------------------
def get_category_summary(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT categories.name, COUNT(products.id)
        FROM categories
        LEFT JOIN products ON products.category_id = categories.id
        GROUP BY categories.id
    """)
    return cur.fetchall()


# ---------------------------------------------------------
# Top Value Products (qty × price)
# ---------------------------------------------------------
def get_top_value_products(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT name, quantity, unit_price
        FROM products
        ORDER BY (quantity * unit_price) DESC
    """)
    return cur.fetchall()


# ---------------------------------------------------------
# Dashboard Summary
# ---------------------------------------------------------
def dashboard_summary(conn):
    print("\n=== Dashboard Summary ===")

    # -------------------------
    # Total Inventory Value
    # -------------------------
    total_value = get_inventory_value(conn)
    print(f"Total Inventory Value: ${total_value:.2f}")

    # -------------------------
    # Low Stock Alerts
    # -------------------------
    low_stock = get_low_stock_products(conn)

    print("\nLow Stock Alerts:")
    if not low_stock:
        print("- All products are sufficiently stocked.")
    else:
        for p in low_stock:
            print(f"- {p[1]} (Qty: {p[2]}) is running low!")

    # Summary count
    if len(low_stock) == 0:
        print(f"Low Stock Items: {GREEN}0 (All good){RESET}")
    elif len(low_stock) < 5:
        print(f"Low Stock Items: {YELLOW}{len(low_stock)} (Monitor soon){RESET}")
    else:
        print(f"Low Stock Items: {RED}{len(low_stock)} (Critical){RESET}")

    # -------------------------
    # Supplier Count
    # -------------------------
    supplier_counts = get_supplier_counts(conn)
    print(f"Total Suppliers: {len(supplier_counts)}")

    # -------------------------
    # Category Count
    # -------------------------
    category_summary = get_category_summary(conn)
    print(f"Total Categories: {len(category_summary)}")

    # -------------------------
    # Top Value Products
    # -------------------------
    top_products = get_top_value_products(conn)

    print("\nTop Value Products:")
    for p in top_products[:5]:
        name = p[0]
        qty = p[1]
        price = p[2]
        value = qty * price

        color = GREEN
        if value > 500:
            color = YELLOW
        if value > 2000:
            color = RED

        print(f"- {color}{name} (${price:.2f} each, Qty: {qty}, Value: ${value:.2f}){RESET}")

    print("\nDashboard loaded successfully.\n")

import csv

def export_products_to_csv(conn, filename="products_export.csv"):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.name, p.quantity, p.price, 
               c.name AS category, s.name AS supplier
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN suppliers s ON p.supplier_id = s.id
    """)
    rows = cursor.fetchall()

    if not rows:
        print("No products to export.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Quantity", "Price", "Category", "Supplier"])
        writer.writerows(rows)

    print(f"Products exported successfully to {filename}")

