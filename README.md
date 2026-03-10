# POS Demo FastAPI

This is a simple Point of Sale (POS) API built with FastAPI, SQLAlchemy, and SQLite.

## Project Structure

```text
app/
├── __init__.py
├── main.py          # FastAPI app initialization
├── models.py        # SQLAlchemy models
├── schemas.py       # Pydantic schemas
├── database.py      # Database connection setup
├── crud.py          # Create, Read, Update, Delete logic
└── routers/         # API route handlers
    ├── __init__.py
    ├── items.py
    └── sales.py
requirements.txt     # Project dependencies
```

## Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the server using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

## Learning Objectives

- Understand FastAPI's dependency injection system (e.g., `get_db`).
- Use SQLAlchemy for ORM with SQLite.
- Implement data validation using Pydantic schemas.
- Organize code using FastAPI routers.
