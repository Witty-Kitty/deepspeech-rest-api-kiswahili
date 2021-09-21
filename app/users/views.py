from datetime import datetime

from sanic.exceptions import Unauthorized
from sanic.response import json as sanic_json, HTTPResponse
from sanic_jwt import protected, inject_user
from sanic_validation import validate_json

from app.database import scoped_session
from app.models import User
from app.responses import Response
from app.users import users_bp
from app.users.schema import create_user_schema, update_user_schema


@users_bp.route('/register', methods=['POST'])
@validate_json(create_user_schema)
async def register_user(request) -> HTTPResponse:
    """ Creates a user in the DB """

    data = request.json or {}
    with scoped_session() as session:
        if session.query(User).filter(User.username == data['username']).first():
            return sanic_json(Response('Please use a different username.').__dict__, status=400)
        if session.query(User).filter(User.email == data['email']).first():
            return sanic_json(Response('Please use a different email address.').__dict__, status=400)
        user = User()
        user.from_dict(data)
        session.add(user)
        session.commit()
        return sanic_json(user.to_dict(), status=200)


@users_bp.route('/<id>', methods=['GET'])
@inject_user()
@protected()
async def get_user(request, id, user) -> HTTPResponse:
    """ Retrieves from the DB a particular user using his `id` """

    if user:
        if user.id == int(id):
            with scoped_session() as session:
                user = session.query(User).filter(User.id == int(id)).first()
                return sanic_json(user.to_dict())
        else:
            raise Unauthorized('Unauthorized access.', status_code=400)
    else:
        raise Unauthorized('Please provide credentials.', status_code=400)


@users_bp.route('/<id>', methods=['PUT'])
@validate_json(update_user_schema)
@inject_user()
@protected()
async def update_user(request, id, user) -> HTTPResponse:
    """ Updates an already existing user """

    if user:
        if user.id != int(id):
            raise Unauthorized('Unauthorized access.', status_code=400)
        with scoped_session() as session:
            ret_user = session.query(User).filter(User.id == int(id)).first()
            data = request.json or {}
            if 'username' in data and data['username'] != ret_user.username and session.query(User).filter(
                    User.username == data['username']).first():
                return sanic_json(Response('Please use a different username.').__dict__, status=400)
            if 'email' in data and data['email'] != ret_user.email and session.query(User).filter(
                    User.email == data['email']).first():
                return sanic_json(Response('Please use a different email address.').__dict__, status=400)
            if 'password' in data:
                user.set_password(data['password'])
                session.query(User).filter(User.id == int(id)).update(
                    {User.username: data['username'], User.email: data['email'],
                     User.password: user.password,
                     User.modified_at: datetime.utcnow()})
                session.commit()
                return sanic_json(Response('User successfully updated.').__dict__, status=200)
            else:
                session.query(User).filter(User.id == int(id)).update(
                    {User.username: data['username'], User.email: data['email'],
                     User.modified_at: datetime.utcnow()})
                session.commit()
                return sanic_json(Response('User successfully updated.').__dict__, status=200)
    else:
        raise Unauthorized('Please provide credentials.', status_code=400)


@users_bp.route('/<id>', methods=['DELETE'])
@inject_user()
@protected()
async def delete_user(request, id, user) -> HTTPResponse:
    """ Deletes an existing user from the DB"""

    if user:
        if user.id == int(id):
            with scoped_session() as session:
                session.query(User).filter(User.id == int(id)).delete()
                return sanic_json(Response('User successfully removed.').__dict__, status=200)
        raise Unauthorized('Unauthorized access.', status_code=400)
    else:
        raise Unauthorized('Please provide credentials.', status_code=400)


@users_bp.route('/', methods=['GET'])
@protected()
async def list_users(request) -> HTTPResponse:
    """ Retrieves all users from the DB"""

    with scoped_session() as session:
        users = session.query(User).all()
        users = [user.to_dict() for user in users]
        return sanic_json(users, status=200)
