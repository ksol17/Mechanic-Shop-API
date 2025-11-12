from flask import Blueprint

mechanics_bp = Blueprint('mechanics', __name__)

@mechanics_bp.route('/')
def index():
    return "Mechanics Blueprint!"
