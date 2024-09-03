from http import HTTPStatus
from flaskr.models.role import Role, db

def test_role_create_sucesso(client, access_token):
    response = client.post('/roles/', json = {'name': 'test'}, headers={'Authorization': f'Bearer {access_token}'})
    
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Role criada'}


def test_role_list_sucesso(client):
    role = Role(name='test')
    db.session.add(role)
    db.session.commit()
    
    lista = []
    for item in lista:
        response = lista.append(client.get('/roles/list'))
    
        assert response.status_code == HTTPStatus.OK
        assert response == [{'id': role.id, 'name':role.name}]
    

def test_role_list_falha(client):
    lista = []
    for item in lista:
        response = lista.append(client.get('/roles/list'))
    
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json == {'msg':'Post inexistente'}