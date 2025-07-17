from app.extensions import db

# Association table for many-to-many between mechanics and service tickets
mechanic_ticket = db.Table(
    'mechanic_ticket',
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True),
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True)
)

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(360), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    service_tickets = db.relationship('ServiceTicket', back_populates='customer')

class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(360), nullable=False, unique=True)

    service_tickets = db.relationship(
        'ServiceTicket',
        secondary=mechanic_ticket,
        back_populates='mechanics'
    )

class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    customer = db.relationship('Customer', back_populates='service_tickets')
    mechanics = db.relationship(
        'Mechanic',
        secondary=mechanic_ticket,
        back_populates='service_tickets'
    )

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)


