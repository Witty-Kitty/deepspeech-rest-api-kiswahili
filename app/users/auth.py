from datetime import datetime, timedelta

from aredis import StrictRedis
from sanic_jwt.exceptions import AuthenticationFailed

from app.database import scoped_session
from app.models import User

aredis = StrictRedis()


async def authenticate(request, *args, **kwargs):
    with scoped_session() as session:
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            raise AuthenticationFailed('Missing username or password.')

        user = session.query(User).filter(User.username == username).first()
        if user is None:
            raise AuthenticationFailed('User not found.')
        if not user.check_password(password):
            raise AuthenticationFailed('Password is incorrect.')
        session.expunge_all()
        return user


async def retrieve_user(request, payload, *args, **kwargs):
    with scoped_session() as session:
        if payload:
            id = payload.get('user_id', None)
            user = session.query(User).filter(User.id == id).first()
            session.expunge_all()
            return user
        else:
            return None


async def extend_payload(payload, user):
    user_id = user.id
    exp = (datetime.now() + timedelta(days=30)).timestamp()
    payload.update({'user_id': user_id, 'exp': exp})
    return payload


# To be revisited as they are causing "aredis.exceptions.ConnectionError"

async def store_refresh_token(user_id, refresh_token, *args, **kwargs):
    key = f'refresh_token_{user_id}'
    await aredis.set(key, refresh_token)


async def retrieve_refresh_token(request, user_id, *args, **kwargs):
    key = f'refresh_token_{user_id}'
    return await aredis.get(key)
