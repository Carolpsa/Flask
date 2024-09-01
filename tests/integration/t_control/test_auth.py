from http import HTTPStatus

def test_auth_user_delete_falha_password(client, cria_usuario):
    user = cria_usuario
    response = client.post(f'/auths/login', json={'username': user.username, 'password': 'incorreto'})
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json == {'msg': 'Bad password'}


def test_auth_user_delete_falha_user(client, cria_usuario):
    user = cria_usuario
    response = client.post(f'/auths/login', json={'username': 'incorreto', 'password': user.password})
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json == {'msg': 'Bad username'}


def test_auth_post_create_falha_password(client, cria_usuario):
    user = cria_usuario
    response = client.post(f'/auths/login', json={'username': user.username, 'password': 'incorreto'})
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json == {'msg': 'Bad password'}


def test_auth_post_create_falha_user(client, cria_usuario):
    user = cria_usuario
    response = client.post(f'/auths/login', json={'username': 'incorreto', 'password': user.password})
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json == {'msg': 'Bad username'}

