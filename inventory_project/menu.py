from db import SessionLocal
from services import adjust_stock
import reports
from models import Product, Category, Supplier

def main_menu():
    session = SessionLocal()

    while True:
        print("\n=== INVENTORY MENU ===")
        print("1. Stock IN")
        print("2. Stock OUT")
        print("3. View Stock Levels")
        print("4. View Movement History")
        print("5. View Inventory Value")
        print("6. Exit")
        print("7. Create Product")

        choice = input("Choose an option: ")

        if choice == "1":
            sku = input("Enter product SKU: ")
            warehouse = input("Enter warehouse name: ")
            qty = int(input("Quantity IN: "))
            cost = float(input("Unit cost: "))
            ref = input("Reference (PO number): ")

            adjust_stock(
                session,
                product_sku=sku,
                warehouse_name=warehouse,
                movement_type="IN",
                quantity=qty,
                unit_cost=cost,
                reference=ref
            )
            print("Stock added.")

        elif choice == "2":
            sku = input("Enter product SKU: ")
            warehouse = input("Enter warehouse name: ")
            qty = int(input("Quantity OUT: "))
            ref = input("Reference (SO number): ")

            adjust_stock(
                session,
                product_sku=sku,
                warehouse_name=warehouse,
                movement_type="OUT",
                quantity=qty,
                reference=ref
            )
            print("Stock removed.")

        elif choice == "3":
            reports.report_stock_levels()

        elif choice == "4":
            reports.report_movement_history()

        elif choice == "5":
            reports.report_inventory_value()

        elif choice == "7":
            name = input("Product name: ")
            sku = input("SKU: ")
            category_name = input("Category name: ")
            supplier_name = input("Supplier name: ")
            cost = float(input("Unit cost: "))

            # Find or create category
            category = session.query(Category).filter_by(name=category_name).one_or_none()
            if category is None:
                category = Category(name=category_name)
                session.add(category)
                session.commit()

            # Find or create supplier
            supplier = session.query(Supplier).filter_by(name=supplier_name).one_or_none()
            if supplier is None:
                supplier = Supplier(name=supplier_name)
                session.add(supplier)
                session.commit()

            # Create product
            product = Product(
                name=name,
                sku=sku,
                category=category,
                supplier=supplier,
                unit_cost=cost
            )
            session.add(product)
            session.commit()

            print("Product created successfully!")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")
