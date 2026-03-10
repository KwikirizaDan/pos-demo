from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    inventory_quantity: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class SaleItemBase(BaseModel):
    item_id: int
    quantity: int

class SaleItemCreate(SaleItemBase):
    pass

class SaleItem(SaleItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sale_id: int
    price_at_sale: float

class SaleBase(BaseModel):
    total_amount: float

class SaleCreate(BaseModel):
    items: List[SaleItemCreate]

class Sale(SaleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: datetime.datetime
    items: List[SaleItem]
