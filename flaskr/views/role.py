from flaskr.app import ma
from flaskr.models.role import Role
from marshmallow import fields

class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role

    id = ma.auto_field()
    name = ma.auto_field()
  
        # Fields to expose
        #fields = ('id', 'name')

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

class CreateRoleSchema(ma.Schema):
    name = fields.String(required=True)

schema_create_role = CreateRoleSchema()