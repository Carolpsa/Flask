from http import HTTPStatus

def test_post_create_sucesso(client, access_token):
    response = client.post('/posts/create',  json={'author_id': 1, 'title': 'test', 'body': 'test'}, headers={'Authorization': f'Bearer {access_token}'})
    
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Post criado'}


def test_post_detail_sucesso(client, cria_post):
    post = cria_post
    
    response = client.get(f'/posts/post{post.id}')
   
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id':post.id, 'author_id': post.author_id, 'title': post.title, 'body': post.body, 'created': post.formatted_created}


def test_post_detail_falha(client):
    post_id = 1
    
    response = client.get(f'/posts/post{post_id}')
   
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'msg': 'Post inexistente'}


def test_post_delete_sucesso(client, access_token, cria_post):
    post = cria_post

    response = client.post(f'/posts/delete{post.id}', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'msg': 'Post deletado'}


def test_post_delete_falha(client, access_token):
    post_id = 1

    response = client.post(f'/posts/delete{post_id}', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'msg':'Post inexistente'}


def test_post_list_sucesso(client, cria_post):
    post = cria_post

    lista = []
    for item in lista:
        response = lista.append(client.get('/posts/list'))

        assert response == [{'id':post.id, 'author_id': post.author_id, 'title': post.title, 'body': post.body, 'created': post.formatted_created}]


def test_post_list_falha(client):
    
    lista = []
    for item in lista:
        response = lista.append(client.get('/posts/list'))

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json == {'msg':'Post inexistente'}


def test_post_update_sucesso_author_id(client, cria_post, access_token):
    post = cria_post
    response = client.patch(f'/posts/update{post.id}', json={'author_id': 2}, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id':post.id, 'author_id': post.author_id, 'title': post.title, 'body': post.body, 'created': post.formatted_created}


def test_post_update_sucesso_title(client, cria_post, access_token):
    post = cria_post
    response = client.patch(f'/posts/update{post.id}', json={'title': 'test2'}, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id':post.id, 'author_id': post.author_id, 'title': post.title, 'body': post.body, 'created': post.formatted_created}


def test_post_update_sucesso_body(client, cria_post, access_token):
    post = cria_post
    response = client.patch(f'/posts/update{post.id}', json={'body': 'test2'}, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id':post.id, 'author_id': post.author_id, 'title': post.title, 'body': post.body, 'created': post.formatted_created}


def test_post_update_falha(client, access_token):
    post_id = 2
    response = client.patch(f'/posts/update{post_id}', json={'body': 'test2'}, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {'msg': 'Post inexistente'}