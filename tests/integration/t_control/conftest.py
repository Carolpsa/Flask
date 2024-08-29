import pytest
from flaskr.app import create_app, db


# A configuracao sera igual ao arquivo app.py e o banco de dados nao ira criar um arquivo, rodara em memoria

@pytest.fixture()
def app():
    app = create_app({
        'SECRET_KEY':'dev',
        'SQLALCHEMY_DATABASE_URI':'sqlite://',
        'JWT_SECRET_KEY': 'test'
    })
    
    with app.app_context():
        db.create_all()
  
        yield app


@pytest.fixture()
def client(app):
    return app.test_client()


# arquivo conftest fica disponivel para todo o modulo integration
# quando o pytest detecta esse arquivo ele executado ele antes de todo o pacote integration