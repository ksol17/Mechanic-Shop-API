from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import db
from app.models import ServiceTicket, Mechanic
from . import service_tickets_bp
from .schemas import ticket_schema, tickets_schema

# Create a new service ticket
@service_tickets_bp.route('/', methods=['POST'])
def create_ticket():
    try:
        data = request.get_json()
        ticket = ticket_schema.load(data)
        db.session.add(ticket)
        db.session.commit()
        return ticket_schema.jsonify(ticket), 201
    except ValidationError as ve:
        return jsonify({"validation_error": ve.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Get all service tickets
@service_tickets_bp.route('/', methods=['GET'])
def get_all_tickets():
    try:
        tickets = ServiceTicket.query.all()
        return tickets_schema.jsonify(tickets), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Assign a mechanic to a ticket
@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get(ticket_id)
    mechanic = Mechanic.query.get(mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()

    return ticket_schema.jsonify(ticket), 200


# Remove a mechanic from a ticket
@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get(ticket_id)
    mechanic = Mechanic.query.get(mechanic_id)

    if not ticket or not mechanic:
        return jsonify({"error": "Ticket or Mechanic not found"}), 404

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()

    return ticket_schema.jsonify(ticket), 200
