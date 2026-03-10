from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime

# --- Item Schemas ---

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    inventory_quantity: int

class ItemCreate(ItemBase):
    """Schema for creating a new item. Inherits from ItemBase."""
    pass

class Item(ItemBase):
    """Schema for reading an item. Includes the ID and ORM configuration."""
    model_config = ConfigDict(from_attributes=True)
    id: int

# --- Sale Item Schemas ---

class SaleItemBase(BaseModel):
    item_id: int
    quantity: int

class SaleItemCreate(SaleItemBase):
    """Schema for adding an item to a sale."""
    pass

class SaleItem(SaleItemBase):
    """Schema for reading a sale item's details."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    sale_id: int
    price_at_sale: float

# --- Sale Schemas ---

class SaleBase(BaseModel):
    total_amount: float

class SaleCreate(BaseModel):
    """Schema for creating a new sale. Requires a list of items to be purchased."""
    items: List[SaleItemCreate]

class Sale(SaleBase):
    """Schema for reading a sale, including its timestamp and the list of items purchased."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: datetime.datetime
    items: List[SaleItem]
