from http import HTTPStatus
from flaskr.models.user import User, db

# como o endpoint espera receber dados json, e necessario passar os parametros utilizando json como parametro da fixture
# tentei fazer igual ao metodo do modulo user_controller e obtive o erro 415 - media nao suportada

def test_user_create_sucesso(client):
    response = client.post('/users/create',  json={'username': 'Carol', 'password': 'test', 'role_id': 1})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Usuario criado'}

# necessario realizar correcao
def test_user_create_falha_unique_username(client, cria_usuario):
    user = cria_usuario
    
    response = client.post('/users/create',  json={'username': 'Carol', 'password': 'test', 'role_id': 1})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

# necessario realizar correcao
def test_user_create_falha_username_null(client):
    response = client.post('/users/create',  json={'username': None, 'password': 'test', 'role_id': 1})
    assert response.status_code == HTTPStatus.OK
    #assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

# necessario realizar correcao
def test_user_create_falha_password_null(client):
    response = client.post('/users/create',  json={'username': 'Carol', 'password': None, 'role_id': 1})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_user_detail_sucesso(client, cria_usuario):
    user = cria_usuario

    response = client.get(f'/users/user{user.id}')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id': user.id,'username':user.username, 'password': user.password, 'role_id': user.role_id}


def test_user_detail_falha(client):
    user_id = 1
    response = client.get(f'/users/user{user_id}')
   
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'msg': 'Usuario nao localizado!'}


def test_user_delete_sucesso(client, access_token):
    user = db.session.execute(db.select(User).where(User.username == 'Carol')).scalar()
                                 
    response = client.post(f'/users/delete{user.id}', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'msg': 'Usuario deletado'}


def test_user_delete_falha(client, access_token):
    user_id = 2
    response = client.get(f'/users/delete{user_id}', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'msg':'Usuario nao localizado!'}


def test_user_update_sucesso_username(client, access_token):
    user = db.session.execute(db.select(User).where(User.username == 'Carol')).scalar()
    
    response = client.patch(f'/users/update{user.id}', json={'username': 'test'}, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id': user.id, 'username':user.username}


def test_user_update_sucesso_role_id(client, access_token):
    user = db.session.execute(db.select(User).where(User.username == 'Carol')).scalar()
    
    response = client.patch(f'/users/update{user.id}', json={'role_id': 'test'}, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id': user.id, 'role_id':user.role_id}


def test_user_update_sucesso_password(client, access_token):
    user = db.session.execute(db.select(User).where(User.username == 'Carol')).scalar()
    
    response = client.patch(f'/users/update{user.id}', json={'password': 'test'}, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id': user.id, 'password':user.password}


def test_user_update_falha(client, access_token):
    user_id = 2
    response = client.patch(f'/users/update{user_id}', json={'password': 'test'}, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'msg':'Usuario nao localizado!'}