from functools import wraps
from flask import request
from http import HTTPStatus
from validate_email import validate_email


class AdminValidator:
    OK = HTTPStatus.OK
    FOUND = HTTPStatus.FOUND
    CREATED = HTTPStatus.CREATED
    NO_CONTENT = HTTPStatus.NO_CONTENT

    NOT_FOUND = HTTPStatus.NOT_FOUND
    BAD_REQUEST = HTTPStatus.BAD_REQUEST
    UNAUTHORIZED = HTTPStatus.UNAUTHORIZED
    INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def login_validator(f):

        @wraps(f)
        def validator(*args, **kwargs):
            body = request.get_json()
            email = body.get('email')
            password = body.get('password')

            if not email:
                return {'message': 'Email not provider'}, AdminValidator.BAD_REQUEST
            if not password:
                return {'message': 'password not provider'}, AdminValidator.BAD_REQUEST

            return f(*args, **kwargs)

        return validator

    @staticmethod
    def create_validator(f):
        @wraps(f)
        def validator(*args, **kwargs):
            body = request.get_json()

            email = body.get("email")
            password = body.get("password")

            is_valid_email = validate_email(email)

            if not email:
                return {'message': 'email not provider'}, AdminValidator.BAD_REQUEST
            if not is_valid_email:
                return {'message': 'Invalid email'}, AdminValidator.BAD_REQUEST
            if not password:
                return {'message': 'password not provider'}, AdminValidator.BAD_REQUEST

            return f(*args, **kwargs)

        return validator
