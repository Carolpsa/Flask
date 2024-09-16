from flaskr.app import ma
from flaskr.models.post import Post
from marshmallow import fields


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        # Fields to expose
        model = Post
        
    id = ma.auto_field()
    author_id = ma.auto_field()
    created = ma.auto_field()
    title = ma.auto_field()
    body = ma.auto_field()
 
   
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class CreatePostSchema(ma.Schema):
    author_id = fields.String(required=True)
    title = fields.String(required=True)
    body = fields.String(required=True)

schema_create_post = CreatePostSchema()