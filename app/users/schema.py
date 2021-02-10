create_user_schema = {
    'username': {'type': 'string', 'minlength': 3, 'maxlength': 127, 'required': True, 'empty': False},
    'email': {'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 'required': True,
              'empty': False},
    'password': {'type': 'string', 'minlength': 8, 'maxlength': 255, 'required': True, 'empty': False}
}

update_user_schema = {
    'username': {'type': 'string', 'minlength': 3, 'maxlength': 127, 'required': False, 'empty': False},
    'email': {'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 'required': False,
              'empty': False},
    'password': {'type': 'string', 'minlength': 8, 'maxlength': 255, 'required': False, 'empty': False}
}
