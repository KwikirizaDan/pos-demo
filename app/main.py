from fastapi import FastAPI
from . import models
from .database import engine
from .routers import items, sales

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="POS Demo API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the POS Demo API"}

app.include_router(items.router)
app.include_router(sales.router)
