# 📘 Name Card API – Flask REST Project

This is a Flask-based web application and REST API for managing business cards.  
It allows users to **add, view, update, and delete** cards via both:

- a simple web UI (`/ui`)
- and a RESTful JSON API (`/api/cards`)

---

## 🚀 Features

- Add/view/delete cards from web interface
- Full REST API (GET, POST, PUT, DELETE)
- SQLite + SQLAlchemy ORM
- JSON API responses
- Simple built-in interface (no extra templates required)
- Full test coverage using `pytest`
- Clean, single-file architecture (`server.py`)

---

## 🔌 REST API Endpoints

| Method   | Endpoint                | Description              |
|----------|-------------------------|--------------------------|
| `GET`    | `/api/cards`            | Get all business cards   |
| `GET`    | `/api/cards/<id>`       | Get a specific card      |
| `POST`   | `/api/cards`            | Add a new card           |
| `PUT`    | `/api/cards/<id>`       | Update an existing card  |
| `DELETE` | `/api/cards/<id>`       | Delete a card            |

---

## 🔧 How to Run the Project

### ✅ Requirements

- Python 3.12
- Flask
- Flask-SQLAlchemy
- pytest (for testing)

---

### 🛠 Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/your-username/name-card-api.git
cd name-card-api

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # on Windows

# 3. Install dependencies
pip install Flask Flask-SQLAlchemy pytest

# 4. Run the app
flask run
```

Then visit:  
[http://127.0.0.1:5000/ui](http://127.0.0.1:5000/ui) — for the visual interface  
[http://127.0.0.1:5000/api/cards](http://127.0.0.1:5000/api/cards) — for the raw API

---

## 🧪 How to Test the API

Use tools like **Postman**, **Thunder Client**, or `curl`.

### ➕ Add a Card (POST)

```bash
POST /api/cards
Content-Type: application/json

{
  "name": "Alice Smith",
  "email": "alice@example.com",
  "phone": "1234567890",
  "company": "CoolCorp",
  "job_title": "Designer"
}
```

### 📝 Update a Card (PUT)

```bash
PUT /api/cards/1
Content-Type: application/json

{
  "email": "newemail@example.com"
}
```

### 🗑 Delete a Card (DELETE)

```bash
DELETE /api/cards/1
```

---

## 🧱 Project Structure

```
02_Name_Card_website/
├── server.py             # Main Flask app with routes + model
├── cards.db              # SQLite database
├── tests/                # Pytest test cases
│   └── test_api.py
└── README.md             # Documentation (this file)
```