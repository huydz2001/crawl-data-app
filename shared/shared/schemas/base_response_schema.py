from marshmallow import Schema, fields

class BaseResponseSchema(Schema):
    success = fields.Boolean()
    data = fields.Raw()
    message = fields.Str()