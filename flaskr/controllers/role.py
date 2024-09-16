from flask import Blueprint, request
from flaskr.models.base import db
from flaskr.models.role import Role
from http import HTTPStatus
from flaskr.views.role import roles_schema, schema_create_role
from marshmallow import ValidationError

appb = Blueprint('role', __name__, url_prefix='/roles')


@appb.route('/', methods=['POST'])
def role_create():
    try:
        data = schema_create_role.load(request.json)
    except ValidationError as error:
        return error.messages

    role = Role(
        name=data['name']
        )
    db.session.add(role)
    db.session.commit()
    return{'msg': 'Role criada'}, HTTPStatus.CREATED


@appb.route('/list')
def role_list():
    roles = db.session.execute(db.select(Role).order_by(Role.id)).scalars()
    return roles_schema.dump(roles) 