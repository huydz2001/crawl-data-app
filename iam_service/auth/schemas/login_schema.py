from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Username cannot be empty")
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Password cannot be empty")
    )