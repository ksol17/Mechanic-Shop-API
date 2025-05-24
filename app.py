from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table
from datetime import date
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Mechanic_Shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a base class for our models
class Base(DeclarativeBase):
    pass
 
#Instantiate your SQLAlchemy database
db = SQLAlchemy(model_class = Base)
db.init_app(app) #adding our db extension to our app



# Association table for the many-to-many relationship between service_tickets and mechanics
service_mechanics = Table(
    'service_mechanics',
    Base.metadata,
    db.Column('ticket_id', db.Integer, ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, ForeignKey('mechanics.id'), primary_key=True)
)

# Models

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)

    service_tickets: Mapped[list["ServiceTicket"]] = relationship(back_populates="customer")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }
    
class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(50), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)

    customer: Mapped["Customer"] = relationship(back_populates="service_tickets")
    mechanics: Mapped[list["Mechanic"]] = relationship(secondary=service_mechanics, back_populates="tickets")

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)

    tickets: Mapped[list["ServiceTicket"]] = relationship(secondary=service_mechanics, back_populates="mechanics")

# Create tables in the database
with app.app_context():
    db.create_all()

# Create Customer (POST/customers)
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    try:
        customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get all Customers (GET/customers)
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers]), 200

# Get Customer by ID (GET/customers/<id>)
@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = db.session.query(Customer, id)
    if customer:
        return jsonify(customer.to_dict()), 200
    return jsonify({"error": "Customer not found"}), 404

# Update Customer (PUT/customers/<id>)
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)

    try:
        db.session.commit()
        return jsonify(customer.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Delete Customer (DELETE/customers/<id>)
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = db.session.query(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"}), 200

# Create Service Ticket (POST/service_tickets)
app.run()