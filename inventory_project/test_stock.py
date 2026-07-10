from db import SessionLocal
from services import adjust_stock

session = SessionLocal()

adjust_stock(
    session,
    product_sku="USB-001",
    warehouse_name="Main Warehouse",
    movement_type="IN",
    quantity=20,
    unit_cost=5.99,
    reference="PO-001"
)

print("Stock updated!")

