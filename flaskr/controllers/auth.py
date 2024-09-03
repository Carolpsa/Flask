from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from http import HTTPStatus
from flaskr.models.base import db
from flaskr.models.user import User
from flaskr.app import bcrypt

appb = Blueprint('auth', __name__, url_prefix='/auths')

def _check_password(password_hash, password_raw):
    return bcrypt.check_password_hash(password_hash, password_raw)


@appb.route('/login', methods=['POST'])
def login():
    data = request.json
    username_json = data['username']
    password_json = data['password']

    try:
        user = db.session.execute(db.select(User).filter_by(username=username_json)).scalar_one()
    except:
        return{'msg': 'Bad username'}, HTTPStatus.UNAUTHORIZED
    if _check_password(user.password, password_json):
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}
    else:
        return {'msg': 'Bad password'}, HTTPStatus.UNAUTHORIZED