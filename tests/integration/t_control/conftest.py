import pytest
from flaskr.app import create_app
from flaskr.models.user import User
from flaskr.models.post import Post
from flaskr.models.role import Role
from flaskr.models.base import db


# A configuracao sera igual ao arquivo app.py e o banco de dados nao ira criar um arquivo, rodara em memoria

@pytest.fixture()
def app():
    app = create_app(environment='testing')
    
    with app.app_context():
        db.create_all()
  
        yield app


@pytest.fixture()
def client(app):
    return app.test_client()


# arquivo conftest fica disponivel para todo o modulo integration
# quando o pytest detecta esse arquivo ele executado ele antes de todo o pacote integration

# funcoes abaixo foram criadas para evitar repeticao de trechos de codigo no modulo test_user

@pytest.fixture()
def cria_usuario():
    role = Role(name='adm')
    db.session.add(role)
    db.session.commit()

    user = User(username='Carol', password='teste', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture()
def access_token(client):
    role = Role(name='adm')
    db.session.add(role)
    db.session.commit()

    user = User(username='Carol', password='teste', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post('/auths/login', json={'username': user.username, 'password': user.password})
    return response.json['access_token']


@pytest.fixture()
def cria_post():
    post = Post(author_id='test', title='test', body = 'test')
    db.session.add(post)
    db.session.commit()

    return post