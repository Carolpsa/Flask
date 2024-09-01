from flask import Blueprint, request
from flaskr.app import db
from flaskr.app import Post
from http import HTTPStatus
from flask_jwt_extended import jwt_required

appb = Blueprint('post', __name__, url_prefix='/posts')

@appb.route('/')
def index():
    return('Posts')


@appb.route('/create', methods=['GET', 'POST'])
@jwt_required()
def post_create():
    data = request.json
          
    if request.method == 'POST':
        post = Post(
            author_id=data['author_id'],
            title=data['title'],
            body=data['body'],
        )
        db.session.add(post)
        db.session.commit()
        return{'msg': 'Post criado'}, HTTPStatus.CREATED
    else:
        return{'post': []}

@appb.route('/post<int:id>')
def post_detail(id):
    try:
        post = db.get_or_404(Post, id)
    except:
        return{'msg': 'Post inexistente'}, HTTPStatus.NOT_FOUND
    return{'id':post.id, 'author_id': post.author_id, 'title': post.title, 'body': post.body, 'created': post.formatted_created}

@appb.route('/delete<int:id>', methods=['POST'])
@jwt_required()
def post_delete(id):
    try:
        post = db.get_or_404(Post, id)
    except:
        return{'msg':'Post inexistente'}, HTTPStatus.NOT_FOUND
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        return{'msg': 'Post deletado'}

@appb.route('/list')
def post_list():
    try:
        posts = db.session.execute(db.select(Post).order_by(Post.id)).scalars()
    except:
        return{'msg' : 'Post inexistente'}, HTTPStatus.NOT_FOUND
    result = []
    for post in posts:
        result.append({'id':post.id, 'author_id': post.author_id, 'title': post.title, 'body': post.body, 'created': post.formatted_created})
    return result

@appb.route('/update<int:id>', methods=['PATCH'])
@jwt_required()
def update_post(id):
    data = request.json
    try:
        post = db.get_or_404(Post, id)
    except:
        return{'msg': 'Post inexistente'}, HTTPStatus.NOT_FOUND
    if 'author_id' in data:
        post.author_id = data['author_id']
        db.session.commit()
        return{'id':post.id, 'author_id': post.author_id, 'title': post.title, 'body': post.body, 'created': post.formatted_created}
    if 'title' in data:
        post.title = data['title']
        db.session.commit()
        return{'id':post.id, 'author_id': post.author_id, 'title': post.title, 'body': post.body, 'created': post.formatted_created}
    if 'body' in data:
        post.body = data['body']
        db.session.commit()
        return{'id':post.id, 'author_id': post.author_id, 'title': post.title, 'body': post.body, 'created': post.formatted_created}

# Authorization: Bearer <access_token>