from sanic import Blueprint

api_bp = Blueprint('api', url_prefix='/api/v1')

from app.api import routes
