from environs import Env

# Reading from the .env file
env = Env()
env.read_env()


class Config(object):
    """

    """

    SANIC_DEBUG: bool = env.bool('SANIC_DEBUG', default=False)
    SANIC_TESTING: bool = env.bool('SANIC_TESTING', default=False)
    SANIC_HOST: str = env.str('SANIC_HOST', default='0.0.0.0')
    SANIC_PORT: int = env.int('SANIC_PORT', default=8000)
    SANIC_ENV: str = env.str('SANIC_ENV', default='dev')


class DevelopmentConfig(Config):
    """

    """

    SANIC_DEBUG: bool = env.bool('SANIC_DEBUG', default=True)


class TestingConfig(Config):
    """

    """

    SANIC_TESTING: bool = env.bool('SANIC_TESTING', default=False)


class ProductionConfig(Config):
    """

    """

    SANIC_DEBUG: bool = env.bool('SANIC_DEBUG', default=False)
