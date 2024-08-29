from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from http import HTTPStatus
from flaskr.app import db
from flaskr.app import User

appb = Blueprint('auth', __name__, url_prefix='/auths')

@appb.route("/login", methods=["POST"])
def login():
    data = request.json
    username_json = data["username"]
    password_json = data["password"]

    try:
        user = db.session.execute(db.select(User).filter_by(username=username_json)).scalar_one()
    except:
        return{"msg": "Bad username"}, HTTPStatus.UNAUTHORIZED
    try:
        password = db.session.execute(db.select(User).filter_by(password=password_json)).scalar_one()
    except:
        return {"msg": "Bad password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=user.id)
    return {'access_token': access_token}