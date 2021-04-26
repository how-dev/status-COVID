from functools import wraps
from flask import request
from os import getenv
import jwt


def private_route(f):
    @wraps(f)
    def verify_token(*args, **kwargs):
        token = request.headers.get('Authorization')

        secret = getenv("TOKEN_SECRET")

        if not token:
            return {'message': 'Token não providenciado'}
        else:
            try:
                token = token.split(" ")[1]

                is_valid = jwt.decode(token, secret, algorithms=["HS256"])

                if is_valid:
                    return f(*args, **kwargs)
                else:
                    return {'message': 'Token inválido'}
            except Exception as e:
                print(e)
                return {"message": 'Token invalido'}

    return verify_token
