# suppliers.py

import sqlite3


# ---------------------------------------------------------
# Add Supplier
# ---------------------------------------------------------
def add_supplier(conn):
    cur = conn.cursor()
    try:
        name = input("Supplier name: ")
        contact = input("Contact info: ")

        cur.execute("""
            INSERT INTO suppliers (name, contact)
            VALUES (?, ?)
        """, (name, contact))

        conn.commit()
        print("Supplier added successfully.")
    except Exception as e:
        print("Error adding supplier:", e)


# ---------------------------------------------------------
# View Suppliers
# ---------------------------------------------------------
def view_suppliers(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM suppliers")
        rows = cur.fetchall()

        print("\n=== Supplier List ===")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Contact: {row[2]}")
        print()
    except Exception as e:
        print("Error viewing suppliers:", e)


# ---------------------------------------------------------
# Edit Supplier
# ---------------------------------------------------------
def edit_supplier(conn):
    cur = conn.cursor()
    try:
        supplier_id = input("Enter Supplier ID to edit: ")

        cur.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,))
        supplier = cur.fetchone()

        if not supplier:
            print("Supplier not found.")
            return

        print(f"Current Name: {supplier[1]}")
        print(f"Current Contact: {supplier[2]}")

        new_name = input("New name (leave blank to keep current): ") or supplier[1]
        new_contact = input("New contact (leave blank to keep current): ") or supplier[2]

        cur.execute("""
            UPDATE suppliers
            SET name = ?, contact = ?
            WHERE id = ?
        """, (new_name, new_contact, supplier_id))

        conn.commit()
        print("Supplier updated successfully.")

    except Exception as e:
        print("Error editing supplier:", e)


# ---------------------------------------------------------
# Delete Supplier
# ---------------------------------------------------------
def delete_supplier(conn):
    cur = conn.cursor()
    try:
        supplier_id = input("Enter Supplier ID to delete: ")

        cur.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,))
        supplier = cur.fetchone()

        if not supplier:
            print("Supplier not found.")
            return

        confirm = input(f"Are you sure you want to delete '{supplier[1]}'? (y/n): ")
        if confirm.lower() != "y":
            print("Deletion cancelled.")
            return

        cur.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
        conn.commit()
        print("Supplier deleted successfully.")

    except Exception as e:
        print("Error deleting supplier:", e)


# ---------------------------------------------------------
# Search Supplier
# ---------------------------------------------------------
def search_supplier(conn):
    cur = conn.cursor()
    try:
        keyword = input("Enter supplier name or keyword: ")

        cur.execute("""
            SELECT * FROM suppliers
            WHERE name LIKE ?
        """, ('%' + keyword + '%',))

        rows = cur.fetchall()

        if not rows:
            print("No suppliers found.")
            return

        print("\n=== Search Results ===")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Contact: {row[2]}")
        print()

    except Exception as e:
        print("Error searching suppliers:", e)


# ---------------------------------------------------------
# Choose Supplier (used by products.py)
# ---------------------------------------------------------
def choose_supplier(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM suppliers")
    rows = cur.fetchall()

    if not rows:
        print("No suppliers found. Add one first.")
        return None

    print("\n=== Choose a Supplier ===")
    for row in rows:
        print(f"{row[0]}. {row[1]}")

    while True:
        try:
            choice = int(input("Enter supplier ID: "))
            if any(row[0] == choice for row in rows):
                return choice
            else:
                print("Invalid supplier ID. Try again.")
        except ValueError:
            print("Please enter a valid number.")
