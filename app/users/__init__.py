from sanic import Blueprint

users_bp = Blueprint('users', url_prefix='/users')

from app.users import views
