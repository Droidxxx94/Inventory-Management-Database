import sqlite3
from inventory.db import connect_db, create_tables
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
    """)
    rows = cur.fetchall()

    print("\n=== Product List ===")
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Quantity: {row[2]}")
        print(f"Unit Price: ${row[3]:.2f}")
        print(f"Supplier: {row[4]}")
        print(f"Category: {row[5]}")
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

        # ⭐ Category selection goes HERE
        print("\nAssign a category:")
        category_id = choose_category(conn)

        # ⭐ Supplier selection goes HERE
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
        new_name = input("New name (leave blank to keep current): ")
        if new_name == "":
            new_name = product[1]

        print(f"Current Quantity: {product[2]}")
        new_quantity = input("New quantity (leave blank to keep current): ")
        if new_quantity == "":
            new_quantity = product[2]
        else:
            new_quantity = int(new_quantity)

        print(f"Current Unit Price: {product[3]}")
        new_price = input("New price (leave blank to keep current): ")
        if new_price == "":
            new_price = product[3]
        else:
            new_price = float(new_price)

        # ⭐ Category selection goes HERE
        change_cat = input("Change category? (y/n): ")
        if change_cat.lower() == "y":
            new_category_id = choose_category(conn)
        else:
            new_category_id = product[5]

        # ⭐ Supplier selection goes HERE
        change_sup = input("Change supplier? (y/n): ")
        if change_sup.lower() == "y":
            new_supplier_id = choose_supplier(conn)
        else:
            new_supplier_id = product[4]

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
# Search Products Functions
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

def choose_category(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM categories")
    rows = cur.fetchall()

    if not rows:
        print("No categories found. Add one first.")
        return None

    print("\n=== Choose a Category ===")
    for row in rows:
        print(f"{row[0]}. {row[1]}")

    while True:
        try:
            choice = int(input("Enter category ID: "))
            if any(row[0] == choice for row in rows):
                return choice
            else:
                print("Invalid category ID. Try again.")
        except ValueError:
            print("Please enter a valid number.")


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


# ============================
# Supplier Management Functions
# ============================

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

        new_name = input("New name (leave blank to keep current): ")
        new_contact = input("New contact (leave blank to keep current): ")

        if new_name == "":
            new_name = supplier[1]
        if new_contact == "":
            new_contact = supplier[2]

        cur.execute("""
            UPDATE suppliers
            SET name = ?, contact = ?
            WHERE id = ?
        """, (new_name, new_contact, supplier_id))

        conn.commit()
        print("Supplier updated successfully.")

    except Exception as e:
        print("Error editing supplier:", e)

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

# ====================
# Category Functions
# ====================

def add_category(conn):
    cur = conn.cursor()
    try:
        name = input("Category name: ")

        cur.execute("""
            INSERT INTO categories (name)
            VALUES (?)
        """, (name,))

        conn.commit()
        print("Category added successfully.")
    except Exception as e:
        print("Error adding category:", e)

def view_categories(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM categories")
        rows = cur.fetchall()

        print("\n=== Category List ===")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}")
        print()
    except Exception as e:
        print("Error viewing categories:", e)

def edit_category(conn):
    cur = conn.cursor()
    try:
        category_id = input("Enter Category ID to edit: ")

        cur.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        category = cur.fetchone()

        if not category:
            print("Category not found.")
            return

        print(f"Current Name: {category[1]}")
        new_name = input("New name (leave blank to keep current): ")

        if new_name == "":
            new_name = category[1]

        cur.execute("""
            UPDATE categories
            SET name = ?
            WHERE id = ?
        """, (new_name, category_id))

        conn.commit()
        print("Category updated successfully.")

    except Exception as e:
        print("Error editing category:", e)

def delete_category(conn):
    cur = conn.cursor()
    try:
        category_id = input("Enter Category ID to delete: ")

        cur.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        category = cur.fetchone()

        if not category:
            print("Category not found.")
            return

        confirm = input(f"Are you sure you want to delete '{category[1]}'? (y/n): ")
        if confirm.lower() != "y":
            print("Deletion cancelled.")
            return

        cur.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        print("Category deleted successfully.")

    except Exception as e:
        print("Error deleting category:", e)

def search_category(conn):
    cur = conn.cursor()
    try:
        keyword = input("Enter category name or keyword: ")

        cur.execute("""
            SELECT * FROM categories
            WHERE name LIKE ?
        """, ('%' + keyword + '%',))

        rows = cur.fetchall()

        if not rows:
            print("No categories found.")
            return

        print("\n=== Search Results ===")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}")
        print()

    except Exception as e:
        print("Error searching categories:", e)

    def choose_category(conn):
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM categories")
        rows = cur.fetchall()

    if not rows:
        print("No categories found. Add one first.")
        return None

    print("\n=== Choose a Category ===")
    for row in rows:
        print(f"{row[0]}. {row[1]}")

    while True:
        try:
            choice = int(input("Enter category ID: "))
            if any(row[0] == choice for row in rows):
                return choice
            else:
                print("Invalid category ID. Try again.")
        except ValueError:
            print("Please enter a valid number.")
  

def supplier_menu(conn):
    while True:
        print("\n=== Supplier Management ===")
        print("1. Add Supplier")
        print("2. View Suppliers")
        print("3. Edit Supplier")
        print("4. Delete Supplier")
        print("5. Search Supplier")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            add_supplier(conn)
        elif choice == "2":
            view_suppliers(conn)
        elif choice == "3":
            edit_supplier(conn)
        elif choice == "4":
            delete_supplier(conn)
        elif choice == "5":
            search_supplier(conn)
        elif choice == "6":
            break
        else:
            print("Invalid option. Please try again.")

def category_menu(conn):
    while True:
        print("\n=== Category Management ===")
        print("1. Add Category")
        print("2. View Categories")
        print("3. Edit Category")
        print("4. Delete Category")
        print("5. Search Category")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            add_category(conn)
        elif choice == "2":
            view_categories(conn)
        elif choice == "3":
            edit_category(conn)
        elif choice == "4":
            delete_category(conn)
        elif choice == "5":
            search_category(conn)
        elif choice == "6":
            break
        else:
            print("Invalid option. Please try again.")

def display_results(results):
    if not results:
        print("No products found.")
        return
    
    for item in results:
        print(f"ID: {item[0]} | Name: {item[1]} | Qty: {item[2]} | Price: ${item[3]}")


def search_menu(conn):
    while True:
        print("\n=== Product Search ===")
        print("1. Search by Name or ID")
        print("2. Search by Category")
        print("3. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            keyword = input("Enter product name or ID: ")
            results = search_products(conn, keyword)
            display_results(results)

        elif choice == "2":
            search_products_by_category(conn)

        elif choice == "3":
            break

        else:
            print("Invalid option. Try again.")

def search_products_by_category(conn):
    cur = conn.cursor()

    # Show category list
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
        print("9. Supplier Management")
        print("10. Search Products")
        print("11. Category Management")
        choice = input("Choose an option: ")

        if choice == "1":
            view_products(conn)

        elif choice == "2":
            add_product(conn)

        elif choice == "3":
            edit_product(conn)

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

        elif choice == "9":
            supplier_menu(conn)

        elif choice == "10":
            search_menu(conn) 

        elif choice == "11":
            category_menu(conn)


        else:
            print("Invalid option. Please try again.")





# ---------------------------------------------------------
# Program Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    conn = connect_db()
    print("CONNECTION:", conn)   # TEMP DEBUG

    if conn is None:
        print("Database failed to connect.")
        exit()

    create_tables(conn)          # REQUIRED
    add_timestamp_column(conn)
    main_menu(conn)
