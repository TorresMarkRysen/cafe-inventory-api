# Cafe Order & Inventory REST API

A persistent backend CRUD and inventory management API built with **FastAPI**, **SQLModel**, and **SQLite**. Designed to handle catalog items, manage stock levels, and log sales transactions.

---

## Features

- **Persistent Storage:** SQLite database management using SQLModel ORM with context-managed sessions.
- **Input Validation & Integrity:**
  - Prevents invalid values using Pydantic Field constraints (e.g., non-negative stock, price > 0).
  - Uses dedicated request schemas (`OrderRequest`, `RestockRequest`) for transactional actions.
- **Business Logic Guards:**
  - **Duplicate Prevention:** Rejects duplicate catalog entries (`409 Conflict`).
  - **Stock Guards:** Prevents orders that exceed available on-hand inventory (`400 Bad Request`).
  - **Automated Sales Logging:** Deducts inventory, auto-calculates total order cost, and creates a persistent sale record.
  - **Resource Handling:** Validates item existence before updates or deletions (`404 Not Found`).
- **Interactive Documentation:** Out-of-the-box Swagger UI (`/docs`) and ReDoc (`/redoc`) for endpoint testing.

---

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **ORM / Database:** SQLModel (SQLAlchemy) & SQLite
- **ASGI Server:** Uvicorn

---

## API Endpoints

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/menu` | List all menu items and stock levels | `200 OK` |
| `POST` | `/menu` | Add a new item to the menu | `201 Created` / `409 Conflict` |
| `DELETE` | `/menu/{item_name}` | Remove an item from the menu | `200 OK` / `404 Not Found` |
| `PATCH` | `/menu/restock` | Increment stock quantity for an item | `200 OK` / `404 Not Found` |
| `POST` | `/order` | Place an order, decrement stock, log sale | `201 Created` / `400 Bad Request` |
| `GET` | `/sale` | View historical order transactions | `200 OK` |

---

## Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/TorresMarkRysen/cafe-inventory-api.git
cd cafe-inventory-api
## Quickstart

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
