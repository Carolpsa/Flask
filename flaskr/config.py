import os

# classe mae de configuracao
class Config:
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


# ambiente de producao
# Utiliza a config conforme classe acima
# configurar as variaveis de ambiente no render tambem
# gerar valores seguros para as chaves, isso pode ser feito no site passwordsgenerator
class ProductionConfig(Config):
    pass

# ambiente de desenvolvimento
class DevelopmentConfig(Config):
    SECRET_KEY='dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI='sqlite:///blog.sqlite'
    JWT_SECRET_KEY = 'super-secret'

# ambiente de teste
class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI ='sqlite://'
    JWT_SECRET_KEY = 'test'
    