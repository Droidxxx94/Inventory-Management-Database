# main.py

from inventory.db import connect_db, create_tables
from inventory.products import (
    view_products, add_product, edit_product, delete_product,
    restock_product, reduce_stock
)
from inventory.suppliers import (
    add_supplier, view_suppliers, edit_supplier,
    delete_supplier, search_supplier
)
from inventory.categories import (
    add_category, view_categories, edit_category,
    delete_category, search_category
)
from inventory.search import (
    search_products, search_products_by_category,
    search_products_by_supplier, search_products_by_price_range,
    search_low_stock_products, search_products_by_category_name,
    search_products_by_inventory_value
)
from inventory.reports import dashboard_summary, export_products_to_csv

from dashboard import view_dashboard

from dashboard import dashboard_menu

from dashboard import auto_snapshot
auto_snapshot()



# ---------------------------------------------------------
# Product Menu
# ---------------------------------------------------------
def product_menu(conn):
    while True:
        print("\n=== Product Management ===")
        print("1. View Products")
        print("2. Add Product")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. Restock Product")
        print("6. Reduce Stock")
        print("7. Back to Main Menu")

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
            product_id = input("Product ID: ")
            amount = int(input("Amount to add: "))
            if restock_product(conn, product_id, amount):
                print("Product restocked.")
            else:
                print("Error: Product not found.")
        elif choice == "6":
            product_id = input("Product ID: ")
            amount = int(input("Amount to remove: "))
            result = reduce_stock(conn, product_id, amount)
            if result == "not_enough":
                print("Error: Not enough stock.")
            elif result:
                print("Stock reduced.")
            else:
                print("Error: Product not found.")
        elif choice == "7":
            break
        else:
            print("Invalid option.")


# ---------------------------------------------------------
# Supplier Menu
# ---------------------------------------------------------
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
            print("Invalid option.")


# ---------------------------------------------------------
# Category Menu
# ---------------------------------------------------------
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
            print("Invalid option.")


# ---------------------------------------------------------
# Search Menu
# ---------------------------------------------------------
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
            keyword = input("Enter name or ID: ")
            results = search_products(conn, keyword)
            for item in results:
                print(item)

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
            print("Invalid option.")


# ---------------------------------------------------------
# Reports Menu
# ---------------------------------------------------------
def reports_menu(conn):
    while True:
        print("\n=== Reports & Analytics ===")
        print("1. Dashboard Summary")
        print("2. Export Products to CSV")
        print("3. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            dashboard_summary(conn)
        elif choice == "2":
            export_products_to_csv(conn)
        elif choice == "3":
            break
        else:
            print("Invalid option.")


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------
def main():
    conn = connect_db()
    create_tables(conn)

    while True:
        print("\n=== Inventory Management System ===")
        print("1. Products")
        print("2. Suppliers")
        print("3. Categories")
        print("4. Search")
        print("5. Reports")
        print("6. Inventory Dashboard")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            product_menu(conn)
        elif choice == "2":
            supplier_menu(conn)
        elif choice == "3":
            category_menu(conn)
        elif choice == "4":
            search_menu(conn)
        elif choice == "5":
            reports_menu(conn)
        elif choice == "6":
            dashboard_menu(conn)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
