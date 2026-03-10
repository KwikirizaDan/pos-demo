from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

# Create a router for item-related endpoints
router = APIRouter(
    prefix="/items",
    tags=["items"],
)

# Endpoint to create a new item
@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item in the inventory.
    """
    return crud.create_item(db=db, item=item)

# Endpoint to list all items
@router.get("/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all inventory items with optional pagination.
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# Endpoint to get a specific item by ID
@router.get("/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Retrieve details for a specific item by its ID.
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
