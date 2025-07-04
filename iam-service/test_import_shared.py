from shared.utils.jwt_helper import create_token


if __name__ == '__main__':
    token = create_token({'user_id': 123})
    print(token)
