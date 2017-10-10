
class BaseConfig:
    """Base Configuration"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development Configuation"""
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing Configuration"""
    DEBUG = True
    Testing = True


class ProductionConfig(BaseConfig):
    """Production Configuration"""
    DEBUG = False