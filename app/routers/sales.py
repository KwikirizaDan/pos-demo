from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

# Create a router for sales-related endpoints
router = APIRouter(
    prefix="/sales",
    tags=["sales"],
)

# Endpoint to process a new sale
@router.post("/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    """
    Process a new sale transaction, update inventory, and return the sale record.
    """
    return crud.create_sale(db=db, sale=sale)

# Endpoint to list all sales records
@router.get("/", response_model=List[schemas.Sale])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all recorded sales transactions with optional pagination.
    """
    sales = crud.get_sales(db, skip=skip, limit=limit)
    return sales
