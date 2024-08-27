from flask import Blueprint, request
from flaskr.app import db
from flaskr.app import Role
from http import HTTPStatus

appb = Blueprint('role', __name__, url_prefix='/roles')

@appb.route('/', methods=['POST'])
def role_create():
    data = request.json
    role = Role(
        name=data['name']
        )
    db.session.add(role)
    db.session.commit()
    return{'msg': 'Role criada'}, HTTPStatus.CREATED

@appb.route('/list')
def role_list():
    roles = db.session.execute(db.select(Role).order_by(Role.id)).scalars()
    result = []
    for role in roles:
        result.append({"id": role.id, "name":role.name})
    return result