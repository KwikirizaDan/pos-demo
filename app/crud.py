from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

# Fetch a single item by its ID
def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

# Fetch a list of items with optional pagination
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# Create a new inventory item
def create_item(db: Session, item: schemas.ItemCreate):
    # Convert Pydantic model to dictionary and unpack into SQLAlchemy model
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Process a new sale transaction
def create_sale(db: Session, sale: schemas.SaleCreate):
    total_amount = 0
    sale_items = []

    # Check if all requested items exist and if there is sufficient stock
    for item_data in sale.items:
        db_item = get_item(db, item_id=item_data.item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"Item {item_data.item_id} not found")
        if db_item.inventory_quantity < item_data.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough inventory for item {db_item.name}")

        # Calculate amount based on current item price
        price_at_sale = db_item.price
        total_amount += price_at_sale * item_data.quantity

        # Deduct the quantity from inventory stock
        db_item.inventory_quantity -= item_data.quantity

        # Prepare the individual sale item record
        sale_items.append(models.SaleItem(
            item_id=item_data.item_id,
            quantity=item_data.quantity,
            price_at_sale=price_at_sale
        ))

    # Create the master Sale record
    db_sale = models.Sale(total_amount=total_amount)
    db.add(db_sale)

    # Link all prepared sale items to the master Sale record
    for si in sale_items:
        db_sale.items.append(si)
        db.add(si)

    # Atomic transaction: Commit both the stock update and the sale records at once.
    try:
        db.commit()
        db.refresh(db_sale)
    except Exception as e:
        # If any part of the process fails, roll back all changes to maintain data integrity.
        db.rollback()
        raise HTTPException(status_code=500, detail="Transaction failed")

    return db_sale

# Fetch a list of all sale transactions with optional pagination
def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sale).offset(skip).limit(limit).all()
