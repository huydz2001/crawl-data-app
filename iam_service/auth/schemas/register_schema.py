from marshmallow import Schema, fields

class RegisterSchema(Schema):
    username = fields.Str(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Str(required=True)
    role = fields.Str(required=True)