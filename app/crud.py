from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_sale(db: Session, sale: schemas.SaleCreate):
    total_amount = 0
    sale_items = []

    # Check if all items exist and have enough inventory
    for item_data in sale.items:
        db_item = get_item(db, item_id=item_data.item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"Item {item_data.item_id} not found")
        if db_item.inventory_quantity < item_data.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough inventory for item {db_item.name}")

        price_at_sale = db_item.price
        total_amount += price_at_sale * item_data.quantity

        # Update inventory
        db_item.inventory_quantity -= item_data.quantity

        # Prepare SaleItem record (without sale_id yet)
        sale_items.append(models.SaleItem(
            item_id=item_data.item_id,
            quantity=item_data.quantity,
            price_at_sale=price_at_sale
        ))

    # Create the Sale record
    db_sale = models.Sale(total_amount=total_amount)
    db.add(db_sale)

    # Associate sale items
    for si in sale_items:
        db_sale.items.append(si)
        db.add(si)

    # Single commit for atomicity
    try:
        db.commit()
        db.refresh(db_sale)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Transaction failed")

    return db_sale

def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sale).offset(skip).limit(limit).all()
