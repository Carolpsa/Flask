from flask import Blueprint, request
from flaskr.models.user import db, User
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from flaskr.utils import requires_roles
from flaskr.app import bcrypt
from flaskr.views.user import users_schema, user_schema, schema_created_user
from marshmallow import ValidationError

appb = Blueprint('user', __name__, url_prefix='/users')

@appb.route('/')
def index():
    return('Usuarios')



@appb.route('/create', methods=['POST'])
def user_create():
    try:
        data = schema_created_user.load(request.json)
    except ValidationError as error:
        return error.messages

    data = request.json
    user = User(
        username=data['username'],
        password=bcrypt.generate_password_hash(data['password']),
        role_id=data['role_id']
    )
    db.session.add(user)
    db.session.commit()
    return{'msg': 'Usuario criado'}, HTTPStatus.CREATED


@appb.route('/user<int:id>')
def user_detail(id):
    try:
        user = db.get_or_404(User, id)
    except:
        return{'msg': 'Usuario nao localizado!'}, HTTPStatus.NOT_FOUND
    #return{'id': user.id,'username':user.username, 'role_id': user.role_id}
    return user_schema.dump(user)

@appb.route('/delete<int:id>', methods=['GET', 'POST'])
@jwt_required()
def user_delete(id):
    try:
        user = db.get_or_404(User, id)
    except:
        return {'msg':'Usuario nao localizado!'}, HTTPStatus.NOT_FOUND
    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return{'msg': 'Usuario deletado'}

@appb.route('/list')
@jwt_required()
@requires_roles('adm')
def user_list():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    # result = []
    # for user in users:
    #     result.append({'id': user.id, 'username':user.username, 'role_id': user.role_id})
    # return result
    return users_schema.dump(users)

@appb.route('/update<int:id>', methods=['PATCH'])
@jwt_required()
def update_user(id):
    data = request.json
    try:
        user = db.get_or_404(User, id)
    except:
        return({'msg':'Usuario nao localizado!'}, HTTPStatus.NOT_FOUND)
    if 'username' in data:
        user.username = data['username']
        db.session.commit()
        #return{'id': user.id,'username':user.username}
        return user_schema.dump(user)
    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password'])
        db.session.commit()
        return{'msg': 'Password atualizado'}
    if 'role_id' in data:
        user.role_id = data['role_id']
        db.session.commit()
        return user_schema.dump(user)
        #return{'id': user.id,'role_id': user.role_id}