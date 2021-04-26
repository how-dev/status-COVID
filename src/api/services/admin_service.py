from flask import current_app
from http import HTTPStatus

from os import getenv
import jwt

from src.api.models import AdminModel


class AdminService:
    OK = HTTPStatus.OK
    CREATED = HTTPStatus.CREATED
    NOT_FOUND = HTTPStatus.NOT_FOUND
    UNAUTHORIZED = HTTPStatus.UNAUTHORIZED
    INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def login(email, password):
        admin: AdminModel = AdminModel.query.filter_by(email=email).first()

        if admin:
            try:
                is_correct_pass = admin.password_check(password)

                if is_correct_pass:
                    secret = getenv("TOKEN_SECRET")

                    token = jwt.encode({"id": admin.id, "nome": admin.name, "admin": True}, secret)

                    return {'id': admin.id, 'name': admin.name, 'token': token}, AdminService.OK
                else:
                    return {'message': 'Wrong email or password'}, AdminService.UNAUTHORIZED

            except:
                return {'message': 'Internal error'}, AdminService.INTERNAL_SERVER_ERROR

        else:
            return {'message': 'User does not exists'}, AdminService.NOT_FOUND

    @staticmethod
    def create(body):
        session = current_app.db.session

        name = body.get("name")
        email = body.get("email")
        password = body.get("password")

        new_admin = AdminModel(
            name=name,
            email=email,
        )

        new_admin.password = password

        session.add(new_admin)
        session.commit()

        return {
            "admin": {
                "id": new_admin.id,
                "name": new_admin.name,
                "email": new_admin.email
            }
        }, AdminService.CREATED
