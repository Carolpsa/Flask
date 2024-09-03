import os
#import click
from flask import Flask, current_app
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flaskr.models.base import db

migrate = Migrate()
jwt = JWTManager()

# CONFIGURAR O RENDER sem o grupo dev de dependecia, que contem o pytest e pytest-mock que sao utilizados para testes
# $ poetry install --no-root --without dev
# ENTENDER MELHOR ESSE POETRY INSTALL

# Com a utilizacao do migrate, nao se deve inicializar o db dessa forma, pois gera conflitos

# @click.command('init-db')
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     global db
#     with current_app.app_context():
#         db.create_all()
#     click.echo('Initialized the database.')

def create_app(environment = os.environ['ENVIRONMENT']):
    # necessario incluir a variavel de ambiente ENVIRONMENT no render
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(f'flaskr.config.{environment.title()}Config')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    

    # comando init_db nao deve ser utilizado quando ha o migrate
    #app.cli.add_command(init_db_command)
    
    # inicializacao de extensoes
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # registro do blueprint
    from flaskr.controllers import user_controller, post_controller, auth_controller, role_controller
    app.register_blueprint(user_controller.appb)
    app.register_blueprint(post_controller.appb)
    app.register_blueprint(auth_controller.appb)
    app.register_blueprint(role_controller.appb)
    
    return app

# comandos

# rodar servidor
# poetry run flask --app flaskr.app run --debug

# NAO usar essa inicializacao apos o migrate
# iniciar bd - utilizado uma unica vez para iniciar o banco de dados
# flask --app flaskr.app init-db

# Iniciar o bd migrate
# flask --app flaskr.app db init

# versionar bd
# flask --app flaskr.app db migrate -m "Initial migration."

# aplicar a migracao up
# flask --app flaskr.app db upgrade

# aplicar a migracao down
# flask --app flaskr.app db downgrade

# ativacao do ambiente virtual
# rodar sempre com o ambiente virtual ativado, pois o contrario gera problemas para encontrar e importar modulos
# .venv\Scripts\activate