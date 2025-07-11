from marshmallow import Schema, fields, validate

class RefreshTokenSchema(Schema):
    refresh_token = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Refresh token cannot be empty")
    )