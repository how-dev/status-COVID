from flask import current_app
from http import HTTPStatus
from os import getenv
import jwt

from src.api.models import UserModel, VaccineModel, TestModel


class UserService:
    OK = HTTPStatus.OK
    FOUND = HTTPStatus.FOUND
    CREATED = HTTPStatus.CREATED
    NO_CONTENT = HTTPStatus.NO_CONTENT

    NOT_FOUND = HTTPStatus.NOT_FOUND
    BAD_REQUEST = HTTPStatus.BAD_REQUEST
    UNAUTHORIZED = HTTPStatus.UNAUTHORIZED
    INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def login(email, password):
        user: UserModel = UserModel.query.filter_by(email=email).first()

        if user:
            try:
                is_correct_pass = user.password_check(password)

                if is_correct_pass:
                    secret = getenv("TOKEN_SECRET")

                    token = jwt.encode({'user': {"id": user.id, "nome": user.name}}, secret)

                    return {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'document': user.document,
                        'live_with': user.live_with,
                        'exposed_works': user.exposed_works,
                        'tests_list': [
                            {
                                "date_stamp": test.date_stamp,
                                "result": test.result
                            }
                            for test in user.tests_list
                        ],
                        'vaccines': [
                            {
                                "name": vaccine.name,
                                "record": vaccine.record,
                                "voucher": vaccine.voucher,
                                "verified": vaccine.verified
                            }
                            for vaccine in user.vaccines
                        ],
                        'token': token
                    }, UserService.OK
                else:
                    return {'message': 'Wrong email or password'}, UserService.UNAUTHORIZED

            except:
                return {'message': 'Internal error'}, UserService.INTERNAL_SERVER_ERROR

        else:
            return {'message': 'User does not exists'}, UserService.NOT_FOUND

    @staticmethod
    def delete(user_id):
        session = current_app.db.session
        found_user: UserModel = UserModel.query.get(user_id)

        if not found_user:
            return {'message': 'User does not exists'}, UserService.NOT_FOUND

        session.delete(found_user)
        session.commit()

        return '', UserService.NO_CONTENT

    @staticmethod
    def update(body, user_id):
        try:
            session = current_app.db.session

            name = body["name"]
            email = body["email"]
            document = body["document"]

            found_user: UserModel = UserModel.query.get(user_id)

            found_user.email = email
            found_user.name = name
            found_user.document = document

            session.add(found_user)
            session.commit()

            return {
                       "user": {
                           "id": found_user.id,
                           "name": found_user.name,
                           "age": found_user.age,
                           "email": found_user.email,
                           "document": found_user.document,
                           "live_with": found_user.live_with,
                           "exposed_works": found_user.exposed_works,
                           "vaccines": [
                               {
                                   "name": vacine.name,
                                   "record": vacine.record,
                                   "voucher": vacine.voucher
                               }
                               for vacine in found_user.vaccines
                           ],
                           "tests": [
                               {
                                   "date_stamp": test.date_stamp,
                                   "result": test.result,
                               }
                               for test in found_user.tests_list
                           ]
                       }
                   }, UserService.OK
        except KeyError:
            return {"error": "Verify the request body"}, UserService.BAD_REQUEST

    @staticmethod
    def get(user_id):
        found_user: UserModel = UserModel.query.get(user_id)

        if not found_user:
            return {"error": "User not found"}, UserService.NOT_FOUND

        return {
                   "user": {
                       "id": found_user.id,
                       "name": found_user.name,
                       "age": found_user.age,
                       "email": found_user.email,
                       "document": found_user.document,
                       "live_with": found_user.live_with,
                       "exposed_works": found_user.exposed_works,
                       "vaccines": [
                           {
                               "id": vaccine.id,
                               "name": vaccine.name,
                               "record": vaccine.record,
                               "voucher": vaccine.voucher,
                               "verified": vaccine.verified
                           }
                           for vaccine in found_user.vaccines
                       ],
                       "tests": [
                           {
                               "date_stamp": test.date_stamp,
                               "result": test.result,
                           }
                           for test in found_user.tests_list
                       ]
                   }
               }, UserService.OK

    @staticmethod
    def list_all(user_filter):
        if user_filter:
            list_of_users = (UserModel
                             .query
                             .filter(UserModel.name.like(f"{user_filter}"))
                             .order_by(UserModel.name)
                             .all()
                             )
        else:
            list_of_users = UserModel.query.all()

        return {
                   "users": [
                       {
                           "id": user.id,
                           "name": user.name,
                           "age": user.age,
                           "email": user.email,
                           "document": user.document,
                           "live_with": user.live_with,
                           "exposed_works": user.exposed_works,
                           "vaccines": [
                               {
                                   "name": vacine.name,
                                   "record": vacine.record,
                                   "voucher": vacine.voucher
                               }
                               for vacine in user.vaccines
                           ],
                           "tests": [
                               {
                                   "date_stamp": test.date_stamp,
                                   "result": test.result,
                               }
                               for test in user.tests_list
                           ]
                       }
                       for user in list_of_users
                   ]
               }, UserService.FOUND

    @staticmethod
    def create(body):
        session = current_app.db.session

        name = body.get("name")
        email = body.get("email")
        document = body.get("document")
        age = body.get("age")
        live_with = body.get("live_with")
        exposed_works = body.get("exposed_works")

        password = body.get("password")

        new_user = UserModel(
            name=name,
            email=email,
            document=document,
            age=age,
            live_with=live_with,
            exposed_works=exposed_works
        )
        new_user.password = password

        session.add(new_user)
        session.commit()

        return {
                   "user": {
                       "id": new_user.id,
                       "name": new_user.name,
                       "age": new_user.age,
                       "email": new_user.email,
                       "document": new_user.document,
                       "live_with": new_user.live_with,
                       "exposed_works": new_user.exposed_works,
                       "vaccines": [],
                       "tests": []
                   }
               }, HTTPStatus.CREATED
