from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import db, ma, jwt, limiter, cache
from app.models import ServiceTicket, Mechanic
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema

# Create a new service ticket
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    data = request.get_json()
    ticket = ServiceTicket(
        description=data['description'],
        customer_id=data['customer_id']
    )
    db.session.add(ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 201

# Get all service tickets
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    return service_tickets_schema.jsonify(ServiceTicket.query.all())

# Assign a mechanic to a ticket
@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200


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

    return service_ticket_schema.jsonify(ticket), 200
