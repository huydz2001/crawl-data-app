from marshmallow import Schema, fields

class RefreshTokenSchema(Schema):
    refresh_token = fields.Str(required=True)