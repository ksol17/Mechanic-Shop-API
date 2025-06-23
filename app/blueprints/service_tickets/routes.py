from flask import request, jsonify
from marshmallow import ValidationError
from app.extensions import db, ma, jwt, limiter, cache
from app.models import ServiceTicket, Mechanic
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema

# Create a new service ticket
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        required_fields = ['customer_id', 'mechanic_ids', 'description', 'status']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Ensure mechanic_ids is a list
        mechanic_ids = data.get('mechanic_ids')
        if not isinstance(mechanic_ids, list):
            return jsonify({"error": "mechanic_ids must be a list"}), 400

        # Fetch mechanics and validate all exist
        mechanics = Mechanic.query.filter(Mechanic.id.in_(mechanic_ids)).all()
        if len(mechanics) != len(mechanic_ids):
            return jsonify({"error": "One or more mechanic IDs are invalid"}), 400

        # Create and save the service ticket
        ticket = ServiceTicket(
            customer_id=data['customer_id'],
            description=data['description'],
            status=data['status'],
            mechanics=mechanics
        )
        db.session.add(ticket)
        db.session.commit()

        return jsonify(service_ticket_schema.dump(ticket)), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Get all service tickets
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    tickets = ServiceTicket.query.all()
    return jsonify(service_tickets_schema.dump(tickets)), 200

# Get a single service ticket by ID
@service_tickets_bp.route('/<int:id>', methods=['GET'])
def get_service_ticket(id):
    ticket = ServiceTicket.query.get(id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    return jsonify(service_ticket_schema.dump(ticket)), 200

# Assign a mechanic to a ticket
@service_tickets_bp.route('/assign_mechanic', methods=['POST'])
def assign_mechanic_to_ticket():
    data = request.get_json()
    mechanic_ids = data.get("mechanic_id")
    ticket_id = data.get("ticket_id")

    if not mechanic_ids or not ticket_id:
        return jsonify({"error": "mechanic_id and ticket_id are required"}), 400

    mechanic = Mechanic.query.get(mechanic_ids)
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
    # Update description and status if provided
    ticket.description = data.get('description', ticket.description)
    
    # Update mechanics if mechanic_ids is provided
    mechanic_ids = data.get('mechanic_ids')
    if mechanic_ids is not None:
        if not isinstance(mechanic_ids, list):
            mechanic_ids = [mechanic_ids]
        mechanics = Mechanic.query.filter(Mechanic.id.in_(mechanic_ids)).all()
        if len(mechanics) != len(mechanic_ids):
            return jsonify({"error": "One or more mechanic IDs are invalid"}), 400
        ticket.mechanics = mechanics

    db.session.commit()
    return jsonify({
        "id": ticket.id,
        "description": ticket.description,
        "customer_id": ticket.customer_id
        
    }), 200


# Delete a service ticket
@service_tickets_bp.route('/<int:id>', methods=['DELETE'])
def delete_service_ticket(id):
    ticket = ServiceTicket.query.get(id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Service ticket {id} deleted successfully"}), 200
