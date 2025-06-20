from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.extensions import db, ma, jwt, limiter, cache
from app.models import ServiceTicket, Mechanic
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema

# Create a new service ticket
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    data = request.get_json()
    required_fields = ['customer_id', 'mechanic_id', 'description', 'status']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    service_ticket = ServiceTicket(
        customer_id=data['customer_id'],
        mechanic_id=data['mechanic_id'],
        description=data['description'],
        status=data['status']
    )
    try:
        db.session.add(service_ticket)
        db.session.commit()
        return service_ticket_schema.jsonify(service_ticket), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get all service tickets
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    tickets = ServiceTicket.query.all()
    return service_tickets_schema.jsonify(tickets), 200

# Get a single service ticket by ID
@service_tickets_bp.route('/<int:id>', methods=['GET'])
def get_service_ticket(id):
    ticket = ServiceTicket.query.get(id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    return service_ticket_schema.jsonify(ticket), 200

# Assign a mechanic to a ticket
@service_tickets_bp.route('/assign_mechanic', methods=['POST'])
def assign_mechanic_to_ticket():
    data = request.get_json()
    mechanic_id = data.get("mechanic_id")
    ticket_id = data.get("ticket_id")

    if not mechanic_id or not ticket_id:
        return jsonify({"error": "mechanic_id and ticket_id are required"}), 400

    mechanic = Mechanic.query.get(mechanic_id)
    ticket = ServiceTicket.query.get(ticket_id)

    if not mechanic or not ticket:
        return jsonify({"error": "Mechanic or Ticket not found"}), 404

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()

    return jsonify({"message": "Mechanic assigned to ticket successfully"}), 200

# Update a service ticket
@service_tickets_bp.route('/<int:id>', methods=['PUT'])
def update_service_ticket(id):
    ticket = ServiceTicket.query.get(id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    data = request.get_json()
    if 'description' in data:
        ticket.description = data['description']
    if 'status' in data:
        ticket.status = data['status']
    
    try:
        db.session.commit()
        return service_ticket_schema.jsonify(ticket), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# Delete a service ticket
@service_tickets_bp.route('/<int:id>', methods=['DELETE'])
def delete_service_ticket(id):
    ticket = ServiceTicket.query.get(id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Service ticket {id} deleted successfully"}), 200
