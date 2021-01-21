from sanic import response

from app.users import users_bp


@users_bp.route('/read/<id>')
async def read(request, id):
    return response.json({'identification': id})
