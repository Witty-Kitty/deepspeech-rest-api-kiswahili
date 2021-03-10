from sanic import Sanic

from config import TestingConfig, ProductionConfig, DevelopmentConfig

from sanic import Blueprint

app_bp = Blueprint('app', url_prefix='/')


def create_app() -> Sanic:
    app = Sanic(name='DeepSpeech REST API')

    # Figuring out which between possible server environments
    if app.config['ENV'] == 'dev':
        app.config.update_config(DevelopmentConfig)
    elif app.config['ENV'] == 'prod':
        app.config.update_config(ProductionConfig)
    else:
        app.config.update_config(TestingConfig)

    # Registering all the blueprints
    from app.users import users_bp
    app.blueprint(users_bp)

    from app.api import api_bp
    app.blueprint(api_bp)

    from app.errors import errors_bp
    app.blueprint(errors_bp)

    app.blueprint(app_bp)

    return app


from app.models import User
