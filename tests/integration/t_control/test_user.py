from http import HTTPStatus
from flaskr.app import User, db


# como o endpoint espera receber dados json, e necessario passar os parametros utilizando json como parametro da fixture
# tentei fazer igual ao metodo do modulo user_controller e obtive o erro 415 - media nao suportada

def test_user_create_sucesso(client):
    response = client.post('/users/create',  json={'username': 'Carol', 'password': 'test', 'role_id': 1})
    assert response.status_code == HTTPStatus.CREATED


def test_user_create_falha_unique_username(client, cria_usuario):
    user = cria_usuario
    response = client.post('/users/create',  json={'username': 'Carol', 'password': 'test', 'role_id': 1})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_user_create_falha_username_null(client):
    response = client.post('/users/create',  json={'username': None, 'password': 'test', 'role_id': 1})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_user_create_falha_password_null(client):
    response = client.post('/users/create',  json={'username': 'Carol', 'password': None, 'role_id': 1})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

def test_user_detail_sucesso(client, cria_usuario):
    user = cria_usuario

    response = client.get(f'/users/user{user.id}')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"id": user.id,"username":user.username, "password": user.password, "role_id": user.role_id}


def test_user_detail_falha(client):
    user_id = 1
    response = client.get(f'/users/user{user_id}')
   
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_delete_sucesso(client, access_token):
    user = db.session.execute(db.select(User).where(User.username == 'Carol')).scalar()
                                 
    response = client.post(f'/users/delete{user.id}', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK


def test_user_delete_falha_password(client, cria_usuario):
    user = cria_usuario
    response = client.post(f'/auths/login', json={'username': user.username, 'password': 'incorreto'})
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_user_delete_falha_user(client, cria_usuario):
    user = cria_usuario
    response = client.post(f'/auths/login', json={'username': 'incorreto', 'password': user.password})
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_user_delete_falha_usuario_nao_encontrado(client, access_token):
    response = client.post(f'/users/deleteincorreto', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND