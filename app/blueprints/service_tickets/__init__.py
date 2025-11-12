from flask import Blueprint

service_tickets_bp = Blueprint('service_tickets_bp', __name__)

@service_tickets_bp.route('/')
def index():
    return "Service Tickets Blueprint!"