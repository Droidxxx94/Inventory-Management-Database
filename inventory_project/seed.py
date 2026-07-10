from db import SessionLocal
from models import Category, Supplier, Warehouse, Product

# Open a session
session = SessionLocal()

# Create sample entries
cat = Category(name="Electronics")
sup = Supplier(name="ABC Corp", contact_email="acme@example.com")
wh = Warehouse(name="Main Warehouse", location="Anderson, WI")
prod = Product(
    name="USB Cable",
    sku="USB-001",
    category=cat,
    supplier=sup,
    unit_cost=5.99
)

# Add them to the database
session.add_all([cat, sup, wh, prod])
session.commit()

print("Sample data inserted!")

