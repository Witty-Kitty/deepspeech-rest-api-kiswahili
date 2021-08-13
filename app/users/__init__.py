from sanic import Blueprint

users_bp = Blueprint('users', url_prefix='/api/v1/users')

from app.users import views, schema, auth
