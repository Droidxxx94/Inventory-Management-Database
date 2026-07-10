from sqlalchemy.orm import Session
from models import Product, Warehouse, StockLevel, InventoryMovement

def adjust_stock(
    session: Session,
    product_sku: str,
    warehouse_name: str,
    movement_type: str,   # "IN" or "OUT"
    quantity: int,
    unit_cost=None,
    reference=None
):
    # Find product
    product = session.query(Product).filter_by(sku=product_sku).one()

    # Find warehouse
    warehouse = session.query(Warehouse).filter_by(name=warehouse_name).one()

    # Find existing stock level
    stock = (
        session.query(StockLevel)
        .filter_by(product_id=product.product_id, warehouse_id=warehouse.warehouse_id)
        .one_or_none()
    )

    # If no stock record exists, create one
    if stock is None:
        stock = StockLevel(
            product_id=product.product_id,
            warehouse_id=warehouse.warehouse_id,
            quantity=0
        )
        session.add(stock)

    # Apply movement
    if movement_type == "IN":
        stock.quantity += quantity
    else:  # OUT
        if stock.quantity < quantity:
            raise ValueError("Not enough stock to move OUT")
        stock.quantity -= quantity

    # Record movement
    movement = InventoryMovement(
        product_id=product.product_id,
        warehouse_id=warehouse.warehouse_id,
        movement_type=movement_type,
        quantity=quantity,
        unit_cost=unit_cost,
        reference=reference
    )

    session.add(movement)
    session.commit()

