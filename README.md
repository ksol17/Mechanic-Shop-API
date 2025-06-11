# 🛠️ Mechanic Shop API

A RESTful API built with Flask for managing a mechanic shop. The system supports Customers, Mechanics, Service Tickets and Inventory with full CRUD functionality and relationships between them and secure authentication.

---

## 🚀 Features

- ✅ Application factory pattern for scalable architecture
- ✅ Modular structure using Blueprints
- ✅ SQLAlchemy ORM with type-safe models
- ✅ Marshmallow schemas (using SQLAlchemyAutoSchema)
- ✅ Nested relationship handling (e.g., mechanics and inventory per tickets)
- ✅ Environment-based config loading (dev, test, prod)
- ✅ JWT Token-based Authentication (for customers)
- ✅ Rate Limiting and Caching with Flask-Limiter and Flask-Caching
- ✅ Advanced queries and custome route decorators
- ✅ Secure login system and protected endpoints

---

## ⚙️ Setup Instructions

### 1. 🔧 Install Dependencies

```bash
pip install -r requirements.txt
```
### 2. Create a Virtual Environment
python -m venv .venv
source .venv/bin/activate # On Windows use .venv\Scripts\activate
venv/bin/activate


### 3. Set Configuration
Edit config.py to set your database URI and other settings.
DATABASE_URL=sqlite:///Mechanic_Shop.db


#### 4. Run the Application
```bash
python app.py
```
### 5. Test the API
You can use Postman or curl to test the API endpoints.

---
## 📜 API Endpoints
### Customers
- `GET /customers` – List all customers (paginated)
- `POST /customers` – Create a new customer
- `PUT /customers/<id>` – Update a customer by ID
- `DELETE /customers/<id>` – Delete a customer by ID
- `POST /login` – Customer login (returns token)
- `GET /my-tickets` – Get customer-specific tickets (requires token)

### Mechanics
- `GET /mechanics` – List all mechanics
- `POST /mechanics` – Create a mechanic
- `GET /mechanics/top-mechanics` – Mechanics ranked by number of tickets
- `PUT /mechanics/<id>` – Update mechanic
- `DELETE /mechanics/<id>` – Delete mechanic

### Service Tickets
- `GET /service_tickets` – List all service tickets
- `POST /service_tickets` – Create new ticket
- `PUT /service_tickets/<int:ticket_id>/assign-mechanic/<int:mechanic_id>` – Assign mechanic
- `PUT /service_tickets/<int:ticket_id>/remove-mechanic/<int:mechanic_id>` – Remove mechanic
- `PUT /service_tickets/<int:ticket_id>/edit` – Add/remove multiple mechanics (Advanced)
- `POST /service_tickets/<int:ticket_id>/add-part/<int:part_id>` – Add a part to a ticket

### Inventory
- `GET /inventory` – List all inventory parts
- `POST /inventory` – Create a new inventory part
- `PUT /inventory/<id>` – Update part
- `DELETE /inventory/<id>` – Delete part

---
## 🔐 Security Features
- `encode_token(customer_id)` to generate JWTs
- `@token_required` decorator to protect routes and inject `customer_id`
- Separate `login_schema` using SQLAlchemyAutoSchema (email & password only)
- Optional: mechanic token wrapper for restricted access

---
## 🧠 Advanced Features
- ✅ Pagination on GET customers
- ✅ Mechanics sorted by service ticket count
- ✅ Many-to-many relationships with mechanics and parts
- ✅ Optional: quantity support on inventory-ticket junction table
- ✅ Protected routes for update/delete

---
## 🧪 Technologies Used
- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow (SQLAlchemyAutoSchema)
- Flask-JWT-Extended / python-jose
- Flask-Limiter
- Flask-Caching
- SQLite / PostgreSQL
- Postman

---
## 👩🏽‍💻 Author
Karla Pauta
Made with 💻 and ☕ at Coding Temple 🛠️

