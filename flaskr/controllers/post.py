from flask import Blueprint, request
from flaskr.models.base import db
from flaskr.models.post import Post
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from flaskr.views.post import post_schema, posts_schema, schema_create_post
from marshmallow import ValidationError

appb = Blueprint('post', __name__, url_prefix='/posts')

@appb.route('/')
def index():
    return('Posts')


@appb.route('/create', methods=['POST'])
@jwt_required()
def post_create():
    try:
        data = schema_create_post.load(request.json)
    except ValidationError as error:
        return error.messages
         
    post = Post(
        author_id=data['author_id'],
        title=data['title'],
        body=data['body'],
    )
    db.session.add(post)
    db.session.commit()
    return{'msg': 'Post criado'}, HTTPStatus.CREATED


@appb.route('/post<int:id>')
def post_detail(id):
    try:
        post = db.get_or_404(Post, id)
    except:
        return{'msg': 'Post inexistente'}, HTTPStatus.NOT_FOUND
    return post_schema.dump(post)
    

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

    return posts_schema.dump(posts)


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
        return post_schema.dump(post)
        
    if 'title' in data:
        post.title = data['title']
        db.session.commit()
        return post_schema.dump(post)
        
    if 'body' in data:
        post.body = data['body']
        db.session.commit()
        return post_schema.dump(post)


# Authorization: Bearer <access_token>