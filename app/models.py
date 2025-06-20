from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Customer(db.Model):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[list['ServiceTicket']] = relationship('ServiceTicket', back_populates='customer')

# Association table for many-to-many between mechanics and service tickets
mechanic_ticket = db.Table(
    'mechanic_ticket',
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True),
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True)
)

class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)

    service_tickets: Mapped[list['ServiceTicket']] = relationship(
        'ServiceTicket',
        secondary=mechanic_ticket,
        back_populates='mechanics'
    )

class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(db.String(500), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)

    customer: Mapped['Customer'] = relationship('Customer', back_populates='service_tickets')
    mechanics: Mapped[list['Mechanic']] = relationship(
        'Mechanic',
        secondary=mechanic_ticket,
        back_populates='service_tickets'
    )

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)


