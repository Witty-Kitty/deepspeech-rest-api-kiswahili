from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config

secret_key = Config.SECRET_KEY

Base = declarative_base()


class UserMixin(object):
    """
    Implementations for methods a user object will have
    """

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        """
        Gets the id of the `UserMixin` object
        """
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id()`')

    def __equal__(self, other_object):
        """
        Checks if two  `UserMixin` objects are equal
        """
        if isinstance(other_object, UserMixin):
            return self.get_id() == other_object.get_id()
        return NotImplemented

    def __not_equal__(self, other_object):
        """
        Checks the inequality of two `UserMixin` objects
        """
        equal = self.__equal__(other_object)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


class AnonymousUserMixin(object):
    """
    Default object to represent an anonymous user
    """

    @property
    def is_active(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    username = Column(String(127), index=True, unique=True, nullable=False)
    email = Column(String(127), index=True, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        """ String representation of the user """
        return f'User: {self.username}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() + 'Z',
            'modified_at': self.modified_at.isoformat() + 'Z'
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if 'password' in data:
            self.set_password(data['password'])
