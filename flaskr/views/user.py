from flaskr.app import ma
from flaskr.views.role import RoleSchema
from flaskr.models.user import User
from marshmallow import fields

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    
    id = ma.auto_field()
    username = ma.auto_field()
    
        # Fields to expose
        
    
    role = ma.Nested(RoleSchema)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)

schema_created_user = CreateUserSchema()