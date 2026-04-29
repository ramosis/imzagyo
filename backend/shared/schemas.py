from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True)
    role = fields.Str(default='standart')
    is_admin = fields.Bool(default=False)

user_schema = UserSchema()
