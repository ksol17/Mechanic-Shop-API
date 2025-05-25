# 🛠️ Mechanic Shop API

A RESTful API built with Flask for managing a mechanic shop. The system supports Customers, Mechanics, and Service Tickets with full CRUD functionality and relationships between them.

---

## 🚀 Features

- ✅ Application factory pattern for scalable architecture
- ✅ Modular structure using Blueprints
- ✅ SQLAlchemy ORM with type-safe models
- ✅ Marshmallow schemas for serialization
- ✅ Nested relationship handling (e.g., mechanics assigned to tickets)
- ✅ Environment-based config loading (dev, test, prod)

---

## 🗂️ Project Structure

project_root/
├── app.py # App entry point
├── config.py # Configuration classes
├── .venv # Environment variables
├── app/
│ ├── init.py # Application factory
│ ├── extensions.py # db, ma instances
│ ├── models.py # SQLAlchemy models
│ └── blueprints/
│     ├── customers/
│           ├── init.py # Application factory
│           ├── extensions.py # db, ma instances
│           ├── models.py # SQLAlchemy models
│     ├── mechanics/
│           ├── init.py # Application factory
│           ├── extensions.py # db, ma instances
│           ├── models.py # SQLAlchemy models
│     └── service_tickets/
│           ├── init.py # Application factory
│           ├── extensions.py # db, ma instances
│           ├── models.py # SQLAlchemy models


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
- `GET /customers` - List all customers
- `POST /customers` - Create a new customer
- `PUT /customers/<id>` - Update a customer by ID
- `DELETE /customers/<id>` - Delete a customer by ID
### Mechanics
- `GET /mechanics` - List all mechanics
- `POST /mechanics` - Create a new mechanic
- `PUT /mechanics/<id>` - Update a mechanic by ID
- `DELETE /mechanics/<id>` - Delete a mechanic by ID
### Service Tickets
- `GET /service_tickets` - List all service tickets
- `POST /service_tickets` - Create a new service ticket
- `PUT /service_tickets/<int:ticket_id>/assign-mechanic/<int:mechanic_id>` - Assign a mechanic to a ticket
- `PUT /service_tickets/<int:ticket_id>/remove-mechanic/<int:mechanic_id>` - Remove a mechanic from a ticket


---
## 🧪 Technologies Used
- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- SQLite (or any other SQL database)
- Postman (for testing)

---
## 👩🏽‍💻 Author
Karla Pauta
Made with 💻 and ☕ at Coding Temple 🛠️

