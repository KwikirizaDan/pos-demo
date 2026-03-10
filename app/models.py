from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Item(Base):
    """
    Represents an item in the inventory.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
    inventory_quantity = Column(Integer)

class Sale(Base):
    """
    Represents a single sale transaction.
    """
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    # Automatically set the timestamp to the current time when a sale is created.
    # Note: datetime.datetime.utcnow is used here; for newer Python versions, consider UTC-aware objects.
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Float)

    # Relationship to the items included in this sale
    items = relationship("SaleItem", back_populates="sale")

class SaleItem(Base):
    """
    Represents a specific item and quantity within a sale transaction.
    """
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer)
    # Storing the price at the time of sale to handle future price changes.
    price_at_sale = Column(Float)

    # Back-reference to the parent sale
    sale = relationship("Sale", back_populates="items")
    # Reference to the actual item in the inventory
    item = relationship("Item")
