from sqlalchemy import (
    Column, Integer, String, Boolean, Numeric,
    ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

class Supplier(Base):
    __tablename__ = "suppliers"
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    contact_email = Column(String(150))
    phone = Column(String(50))

class Warehouse(Base):
    __tablename__ = "warehouses"
    warehouse_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    location = Column(String(200))

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"))
    unit_cost = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)

    category = relationship("Category")
    supplier = relationship("Supplier")

class StockLevel(Base):
    __tablename__ = "stock_levels"
    stock_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.warehouse_id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship("Product")
    warehouse = relationship("Warehouse")

class InventoryMovement(Base):
    __tablename__ = "inventory_movements"
    movement_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.warehouse_id"), nullable=False)
    movement_type = Column(String(10), nullable=False)  # IN or OUT
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Numeric(10, 2))
    reference = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    product = relationship("Product")
    warehouse = relationship("Warehouse")

