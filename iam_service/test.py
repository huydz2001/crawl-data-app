# Tạo file test.py trong iam_service/
from auth.schemas import RegisterSchema

test_data = {
    'username': 'test',
    'phone': '0123456789',
    'password': 'password123',
    'email': 'test@example.com',
    'role': 'user'
}

schema = RegisterSchema()
result = schema.load(test_data)
print(f"Test result type: {type(result)}")
print(f"Test result: {result}")