from environs import Env

# Reading from the .env file
env = Env()
env.read_env()


class Config(object):
    """
    These are the default configurations of the API.
    """

    SANIC_DEBUG: bool = env.bool('SANIC_DEBUG', default=False)
    SANIC_TESTING: bool = env.bool('SANIC_TESTING', default=False)
    SANIC_HOST: str = env.str('SANIC_HOST', default='0.0.0.0')
    SANIC_PORT: int = env.int('SANIC_PORT', default=8000)
    SANIC_ENV: str = env.str('SANIC_ENV', default='dev')
    SANIC_FORWARDED_SECRET: str = env.str('SANIC_FORWARDED_SECRET')
    SECRET_KEY: str = env.str('SECRET_KEY')
    DATABASE_URI: str = env.str('DATABASE_URI')


class DevelopmentConfig(Config):
    """
    These configurations are to be used in a development environment.

    This class inherits the default attributes from `Config` and defines
    those that can only be found in development mode.
    """

    DEBUG: bool = env.bool('SANIC_DEBUG')


class TestingConfig(Config):
    """
    These configurations are to be used in a testing environment.

    This class inherits the default attributes from `Config` and defines
    those that can only be found in testing mode.
    """

    TESTING: bool = True


class ProductionConfig(Config):
    """
    These configurations are to be used in a production environment.

    This class inherits the default attributes from `Config` and defines
    those that can only be found in production mode.
    """
    TESTING: bool = False
    DEBUG: bool = False
