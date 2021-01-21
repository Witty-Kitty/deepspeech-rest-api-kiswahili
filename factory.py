from sanic import Sanic

from config import TestingConfig, ProductionConfig, DevelopmentConfig


def create_app():
    app = Sanic(name='DeepSpeech RW API')

    # Choosing between possible server environments
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

    from app import app_bp
    app.blueprint(app_bp)

    return app
