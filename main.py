import sqlite3
from inventory.db import connect_db, create_tables
from inventory.reports import (
    get_inventory_value,
    get_low_stock_items,
    get_supplier_counts,
    get_category_summary,
    get_top_value_products
)

# Terminal color codes
RED = "\033[91m" 
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

CRITICAL_ICON = "❗"
WARNING_ICON = "⚠️"
GOOD_ICON = "✔️"

CRITICAL_ICON = f"{RED}❗{RESET}"
WARNING_ICON  = f"{YELLOW}⚠️{RESET}"
GOOD_ICON     = f"{GREEN}✔️{RESET}"


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
        elif qty < 5:
            icon =WARNING_ICON
        else:
            icon = GOOD_ICON

        print(f"{icon}ID: {row[0]}")
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

def dashboard_summary(conn):
    print("\n=== Dashboard Summary ===")

    # Total inventory value
    total_value = get_inventory_value(conn)
    print(f"Total Inventory Value: ${total_value:.2f}")

    # Low stock count
    low_stock_items = get_low_stock_items(conn)

    if len(low_stock_items) == 0:
        print(f"Low Stock Items: {GREEN}0 (All good){RESET}")
    elif len(low_stock_items) < 5:
        print(f"Low Stock Items: {YELLOW}{len(low_stock_items)} (Monitor soon){RESET}")
    else:
        print(f"Low Stock Items: {RED}{len(low_stock_items)} (Critical){RESET}")

    # Supplier count
    supplier_counts = get_supplier_counts(conn)
    print(f"Total Suppliers: {len(supplier_counts)}")

    # Category count
    category_summary = get_category_summary(conn)
    print(f"Total Categories: {len(category_summary)}")

    # Top 5 highest-value products
    top_products = get_top_value_products(conn)
    print("\nTop Value Products:")
    for p in top_products[:5]:
        value = p[1] * p[2]  # qty * unit_price

        color = GREEN
        if value > 500:
            color = YELLOW
        if value > 2000:
            color = RED

        print(f"- {color}{p[0]} (${p[2]:.2f} each, Qty: {p[1]}, Value: ${value:.2f}){RESET}")

    print("\nDashboard loaded successfully.\n")


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

def search_low_stock_products(conn):
    cur = conn.cursor()

    # You already have low-stock logic in reports, but let's do it directly here
    # so it matches your product search formatting.

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

def search_products_by_category_name(conn):
    cur = conn.cursor()

    keyword = input("Enter category name: ").strip()

    # Find matching categories
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

    # If multiple categories match, ask user which one to use
    try:
        category_id = int(input("Enter the Category ID to view products: "))
    except ValueError:
        print("Invalid input.")
        return

    # Fetch products in that category
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

def make_bar_graph(quantity, max_length=20):
    if quantity <= 0:
        filled = 0
    else:
        filled = int((quantity / max_length) * max_length)
        if filled > max_length:
            filled = max_length

    empty = max_length - filled

    bar = "█" * filled + "░" * empty
    return bar





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

def search_products_by_supplier(conn):
    cur = conn.cursor()

    # Show supplier list
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
        print("3. Search by Supplier")
        print("4. Search by Price Range")
        print("5. Search Low-Stock Products")
        print("6. Search by Category Name")
        print("7. Search by Inventory Value")
        print("8. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            keyword = input("Enter product name or ID: ")
            results = search_products(conn, keyword)
            display_results(results)

        elif choice == "2":
            search_products_by_category(conn)

        elif choice == "3":
            search_products_by_supplier(conn)

        elif choice == "4":
            search_products_by_price_range(conn)

        elif choice == "5":
            search_low_stock_products(conn)

        elif choice == "6":
            search_products_by_category_name(conn)

        elif choice == "7":
            search_products_by_inventory_value(conn)

        elif choice == "8":
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
        print("12. Dashboard Summary")
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

        elif choice == "12":
            dashboard_summary(conn)


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
