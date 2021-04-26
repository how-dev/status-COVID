from functools import wraps
from flask import request
from http import HTTPStatus
from validate_email import validate_email


class UserValidator:
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
                return {'message': 'Email not provider'}, UserValidator.BAD_REQUEST
            if not password:
                return {'message': 'password not provider'}, UserValidator.BAD_REQUEST

            return f(*args, **kwargs)

        return validator

    @staticmethod
    def create_validator(f):
        @wraps(f)
        def validator(*args, **kwargs):
            body = request.get_json()

            name = body.get("name")
            email = body.get("email")
            document = body.get("document")
            age = body.get("age")
            live_with = body.get("live_with")
            exposed_works = body.get("exposed_works")

            password = body.get("password")

            is_valid_email = validate_email(email)
            type_of_age = type(age)
            print(type_of_age)

            if not name:
                return {'message': 'Name not provider'}, UserValidator.BAD_REQUEST
            if not email:
                return {'message': 'email not provider'}, UserValidator.BAD_REQUEST
            if not is_valid_email:
                return {'message': 'Invalid email'}, UserValidator.BAD_REQUEST
            if not document:
                return {'message': 'document not provider'}, UserValidator.BAD_REQUEST
            if not age:
                return {'message': 'age not provider'}, UserValidator.BAD_REQUEST
            if type_of_age != int:
                return {'message': 'age must be a number'}, UserValidator.BAD_REQUEST
            if not live_with:
                return {'message': 'live_with not provider'}, UserValidator.BAD_REQUEST
            if not password:
                return {'message': 'password not provider'}, UserValidator.BAD_REQUEST



            return f(*args, **kwargs)

        return validator
