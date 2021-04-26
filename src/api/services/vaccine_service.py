from flask import current_app
from http import HTTPStatus

from src.api.models import VaccineModel, UserModel


class VaccineService:
    OK = HTTPStatus.OK
    FOUND = HTTPStatus.FOUND
    CREATED = HTTPStatus.CREATED

    NOT_FOUND = HTTPStatus.NOT_FOUND
    BAD_REQUEST = HTTPStatus.BAD_REQUEST

    @staticmethod
    def create(body):
        session = current_app.db.session

        name = body.get("name")
        record = body.get("record")
        voucher = body.get("voucher")
        user_id = body.get("user_id")

        if not name or not record or not voucher or not user_id:
            return {'message': 'Campo obrigatórios não inclusos'}, VaccineService.BAD_REQUEST

        found_user = UserModel.query.get(user_id)

        include_vaccine = VaccineModel(name=name, record=record, voucher=voucher)
        found_user.vaccines.append(include_vaccine)

        session.add(found_user)
        session.commit()

        return {
                   "vaccine": {
                       "id": include_vaccine.id,
                       "name": include_vaccine.name,
                       "record": include_vaccine.record,
                       "voucher": include_vaccine.voucher,
                       "verified": include_vaccine.verified
                   }
               }, VaccineService.CREATED

    @staticmethod
    def list_all(user_id):
        user_vaccines = VaccineModel.query.filter_by(user_id=user_id).all()

        if not user_vaccines:
            return {'message': 'Usuário não encontrado'}, VaccineService.NOT_FOUND

        return {
                   "vaccines":
                       [
                           {
                               "id": vaccine.id,
                               "name": vaccine.name,
                               "record": vaccine.record,
                               "voucher": vaccine.voucher,
                               "verified": vaccine.verified,
                           }
                           for vaccine in user_vaccines
                       ]
               }, VaccineService.FOUND

    @staticmethod
    def update(body, vaccine_id):
        try:
            session = current_app.db.session

            verified = body["verified"]

            found_vaccine: VaccineModel = VaccineModel.query.get(vaccine_id)

            found_vaccine.verified = verified

            session.add(found_vaccine)
            session.commit()

            return {
                "id": found_vaccine.id,
                "name": found_vaccine.name,
                "record": found_vaccine.record,
                "voucher": found_vaccine.voucher,
                "user_id": found_vaccine.user_id,
                "verified": found_vaccine.verified,
            }, VaccineService.OK
        except KeyError:
            return {"error": "Verify the request body"}, VaccineService.BAD_REQUEST
