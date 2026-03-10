from fastapi import FastAPI
from . import models
from .database import engine
from .routers import items, sales

# Create all database tables based on the models defined in models.py
# In a production environment, you would typically use a migration tool like Alembic.
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI(title="POS Demo API")

# Root endpoint
@app.get("/")
def read_root():
    """
    Welcome message for the API.
    """
    return {"message": "Welcome to the POS Demo API"}

# Include routers for different modules
app.include_router(items.router)
app.include_router(sales.router)
