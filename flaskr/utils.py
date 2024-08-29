from flaskr.app import db
from flaskr.app import User
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from functools import wraps


def requires_roles(role_name):
    def decorator(f):
        @wraps(f)
        def envelope(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)
            if user.role.name != role_name:
                return{'msg': 'Role unauthorized'}, HTTPStatus.UNAUTHORIZED
            return f(*args, **kwargs)
        return envelope
    return decorator

# funcao elaborada apenas para teste
def eleva_ao_quadrado(x):
    return x**2