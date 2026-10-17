# Cafe Order & Inventory REST API

A persistent, relational backend API built with **FastAPI**, **SQLModel**, and **SQLite** to manage cafe catalog items, inventory levels, and order transactions.

## Features
- **Persistent Relational Storage:** Backed by SQLite via SQLModel with transactional session handling.
- **Strict Data Validation:** Prevents negative inventory inputs, validates prices, and separates database entities from transient API request schemas.
- **Business Logic Guards:**
  - Prevents duplicate product entries (`409 Conflict`).
  - Guards against orders exceeding current on-hand stock (`400 Bad Request`).
  - Auto-calculates order totals and generates transaction sale records.
- **Interactive Documentation:** Auto-generated Swagger UI for live testing.

## Tech Stack
- Python 3.10+
- FastAPI
- SQLModel / SQLAlchemy
- SQLite
- Uvicorn

## Quickstart

1. Install dependencies:
   ```bash
   pip install -r requirements.txt