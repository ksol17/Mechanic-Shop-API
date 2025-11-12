from flask import Blueprint

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/')
def index():
    return "Customers Blueprint!"