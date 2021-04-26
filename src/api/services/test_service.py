from flask import current_app
from http import HTTPStatus

from src.api.models import TestModel, UserModel


class TestService:
    OK = HTTPStatus.OK
    FOUND = HTTPStatus.FOUND
    CREATED = HTTPStatus.CREATED
    NO_CONTENT = HTTPStatus.NO_CONTENT

    NOT_FOUND = HTTPStatus.NOT_FOUND
    BAD_REQUEST = HTTPStatus.BAD_REQUEST
    UNAUTHORIZED = HTTPStatus.UNAUTHORIZED
    INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def list_all(user_id):
        session = current_app.db.session
        test_found = (
            session
                .query(TestModel.date_stamp, TestModel.result, UserModel.name)
                .join(UserModel)
                .filter(UserModel.id == user_id)
                .all()
        )

        if not test_found:
            return {'message': 'Nenhum teste encontrado'}, TestService.NOT_FOUND

        return {
                   'tests': [
                       {'date_stamp': date_stamp,
                        'result': result,
                        'user': name} for date_stamp, result, name in test_found
                   ]}, TestService.FOUND

    @staticmethod
    def find(test_id):
        found_test: TestModel = TestModel.query.get(test_id)

        if not found_test:
            return {'message': 'Teste não encontrado'}, TestService.NOT_FOUND

        return {
            'test': {
                'date_stamp': found_test.date_stamp,
                'result': found_test.result
            }}, TestService.FOUND

    @staticmethod
    def create(body):
        session = current_app.db.session

        date = body.get('date_stamp')
        result = body.get('result')
        user_id = body.get('user_id')
        image_url = body.get('image_url')

        if not date or result is None or not user_id:
            return {'message': 'Requisição falta argumentos necessários'}, TestService.BAD_REQUEST

        new_test = TestModel(date_stamp=date, result=result, user_id=user_id, image_url=image_url)

        session.add(new_test)
        session.commit()

        return {
            'id': new_test.id,
            'date': new_test.date_stamp,
            'result': new_test.result
        }, TestService.CREATED
