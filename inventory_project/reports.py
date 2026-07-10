from db import SessionLocal
from models import Product, StockLevel, InventoryMovement, Warehouse
from sqlalchemy import func

session = SessionLocal()

# 1. Stock levels by product
def report_stock_levels():
    results = (
        session.query(
            Product.name,
            Product.sku,
            Warehouse.name,
            StockLevel.quantity
        )
        .join(StockLevel, StockLevel.product_id == Product.product_id)
        .join(Warehouse, Warehouse.warehouse_id == StockLevel.warehouse_id)
        .all()
    )

    print("\n=== STOCK LEVELS ===")
    for name, sku, warehouse, qty in results:
        print(f"{name} ({sku}) - {qty} units in {warehouse}")


# 2. Total inventory value
def report_inventory_value():
    results = (
        session.query(
            func.sum(StockLevel.quantity * Product.unit_cost)
        )
        .join(Product, Product.product_id == StockLevel.product_id)
        .scalar()
    )

    print("\n=== TOTAL INVENTORY VALUE ===")
    print(f"${results:.2f}")


# 3. Movement history
def report_movement_history():
    results = (
        session.query(
            InventoryMovement.movement_type,
            InventoryMovement.quantity,
            InventoryMovement.reference,
            InventoryMovement.created_at,
            Product.name,
            Warehouse.name
        )
        .join(Product, Product.product_id == InventoryMovement.product_id)
        .join(Warehouse, Warehouse.warehouse_id == InventoryMovement.warehouse_id)
        .order_by(InventoryMovement.created_at.desc())
        .all()
    )

    print("\n=== MOVEMENT HISTORY ===")
    for mtype, qty, ref, created, pname, wname in results:
        print(f"{created} | {mtype} {qty} of {pname} @ {wname} (Ref: {ref})")


# 4. Low-stock alert (threshold = 5 units)
def report_low_stock(threshold=5):
    results = (
        session.query(
            Product.name,
            Product.sku,
            Warehouse.name,
            StockLevel.quantity
        )
        .join(StockLevel, StockLevel.product_id == Product.product_id)
        .join(Warehouse, Warehouse.warehouse_id == StockLevel.warehouse_id)
        .filter(StockLevel.quantity <= threshold)
        .all()
    )

    print("\n=== LOW STOCK ALERT ===")
    if not results:
        print("All products above threshold.")
        return

    for name, sku, warehouse, qty in results:
        print(f"{name} ({sku}) - ONLY {qty} units left in {warehouse}")

