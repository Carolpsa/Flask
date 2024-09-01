import os
import click

from typing import List
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DateTime
import pytz

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///blog.sqlite',
        JWT_SECRET_KEY = 'super-secret'
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.cli.add_command(init_db_command)
    
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

time_zone = pytz.timezone("America/Sao_Paulo")

class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(time_zone), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    
    user: Mapped['User'] = relationship(back_populates='post') # type: ignore

    @property
    def formatted_created(self):
        return self.created.strftime('%a - %d/%m/%Y %H:%M')

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, author_id={self.author_id!r}, title={self.title!r}, body={self.body!r}, created={self.formatted_created!r})"

class Role(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    user: Mapped[List['User']] = relationship(back_populates='role') # type: ignore

    def __repr__(self) -> str:
        return f"Role (name={self.name!r}, id={self.id!r})"

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'), nullable=False)
    
    
    post: Mapped[List['Post']] = relationship(back_populates='user') # type: ignore
    role: Mapped['Role'] = relationship(back_populates='user') # type: ignore

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"

# comandos

# rodar servidor
# flask --app flaskr.app run --debug

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
# .\projeto_flask\Scripts\activate