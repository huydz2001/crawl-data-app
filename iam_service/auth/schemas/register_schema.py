from marshmallow import Schema, fields, validate, ValidationError

class RegisterSchema(Schema):
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=50, error="Username must be between 3 and 50 characters")
    )
    phone = fields.Str(
        required=True,
        validate=validate.Regexp(r'([\\+84|84|0]+(3|5|7|8|9|1[2689]))+([0-9]{8})$', error="Phone number must be a valid international format")
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, error="Password must be at least 8 characters long")
    )
    email = fields.Email(
        required=True,
        validate=validate.Email(error="Invalid email format"),
    )
    role = fields.Str(
        required=True,
        validate=validate.OneOf(['admin', 'user'], error="Role must be one of: admin, user")
    )