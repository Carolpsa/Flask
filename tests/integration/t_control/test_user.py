from http import HTTPStatus
from flaskr.app import User, db, Role

def test_user_detail_sucesso(client):
    role = Role(name='adm')
    db.session.add(role)
    db.session.commit()

    user = User(username='Carol', password='teste', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.get(f'/users/user{user.id}')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"id": user.id,"username":user.username, "password": user.password, "role_id": user.role_id}


def test_user_detail_falha(client):
    role = Role(name='adm')
    user = User(username='Carol', password='teste', role_id=role.id)

    response = client.get(f'/users/user{user.id}')
   
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_delete_sucesso(client):
    role = Role(name='adm')
    db.session.add(role)
    db.session.commit()

    user = User(username='Carol', password='teste', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post(f'/auths/login', json={'username': user.username, 'password': user.password})
    access_token = response.json['access_token']

    response = client.post(f'/users/delete{user.id}', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK


def test_user_delete_falha_password(client):
    role = Role(name='adm')
    db.session.add(role)
    db.session.commit()

    user = User(username='Carol', password='teste', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post(f'/auths/login', json={'username': user.username, 'password': 'incorreto'})
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_user_delete_falha_user(client):
    role = Role(name='adm')
    db.session.add(role)
    db.session.commit()

    user = User(username='Carol', password='teste', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post(f'/auths/login', json={'username': 'incorreto', 'password': user.password})
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_user_delete_falha_usuario_nao_encontrado(client):
    role = Role(name='adm')
    db.session.add(role)
    db.session.commit()

    user = User(username='Carol', password='teste', role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post(f'/auths/login', json={'username': user.username, 'password': user.password})
    access_token = response.json['access_token']

    response = client.post(f'/users/deleteincorreto', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND