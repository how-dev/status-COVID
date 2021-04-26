from flask import current_app
from http import HTTPStatus
from os import getenv
import jwt

from src.api.models import CompanyModel


class CompanyService:
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
        company: CompanyModel = CompanyModel.query.filter_by(email=email).first()

        if company:
            try:
                is_correct_pass = company.password_check(password)

                if is_correct_pass:
                    secret = getenv("TOKEN_SECRET")

                    token = jwt.encode({'company': {"id": company.id, "name": company.name, "company": True}}, secret)

                    return {
                        'id': company.id,
                        'name': company.name,
                        'email': company.email,
                        'address': company.address,
                        'document': company.document,
                        'token': token
                    }, CompanyService.OK
                else:
                    return {'message': 'Wrong email or password'}, CompanyService.UNAUTHORIZED

            except Exception as e:
                print(e)
                return {'message': "Internal error"}, CompanyService.INTERNAL_SERVER_ERROR

        else:
            return {'message': 'Company does not exists'}, CompanyService.NOT_FOUND

    @staticmethod
    def create(body):
        session = current_app.db.session

        name = body.get("name")
        email = body.get("email")
        document = body.get("document")
        address = body.get("address")

        password = body.get("password")

        if not name or not email or not document or not address or not password:
            return {'message': 'Missing required fields'}, CompanyService.BAD_REQUEST

        new_company = CompanyModel(
            name=name,
            email=email,
            document=document,
            address=address
        )
        new_company.password = password

        session.add(new_company)
        session.commit()

        return {
                   "company": {
                       "id": new_company.id,
                       "name": new_company.name,
                       "address": new_company.address,
                       "email": new_company.email,
                       "document": new_company.document
                   }
               }, HTTPStatus.CREATED

    @staticmethod
    def list_all(company_filter):
        if company_filter:
            list_of_companies = (CompanyModel
                                 .query
                                 .filter(CompanyModel.name.like(f"{company_filter}"))
                                 .order_by(CompanyModel.name)
                                 .all()
                                 )
        else:
            list_of_companies = CompanyModel.query.all()

        return {
                   "companies": [
                       {
                           "id": company.id,
                           "name": company.name,
                           "address": company.address,
                           "email": company.email,
                           "document": company.document
                       }
                       for company in list_of_companies
                   ]
               }, CompanyService.FOUND

    @staticmethod
    def delete(company_id):
        session = current_app.db.session
        found_company: CompanyModel = CompanyModel.query.get(company_id)

        if not found_company:
            return {'message': 'Company does not exists'}, CompanyService.NOT_FOUND

        session.delete(found_company)
        session.commit()

        return '', CompanyService.NO_CONTENT

    @staticmethod
    def update(body, company_id):
        try:
            session = current_app.db.session

            found_company: CompanyModel = CompanyModel.query.get(company_id)

            name = body["name"]
            email = body["email"]
            address = body["address"]

            found_company.email = email
            found_company.name = name
            found_company.address = address

            session.add(found_company)
            session.commit()

            return {
                       "company": {
                           "id": found_company.id,
                           "name": found_company.name,
                           "address": found_company.address,
                           "email": found_company.email,
                           "document": found_company.document
                       }
                   }, CompanyService.OK
        except Exception as e:
            print(e)
            return {"error": "Verify the request body"}, CompanyService.BAD_REQUEST

    @staticmethod
    def get(company_id):
        found_company: CompanyModel = CompanyModel.query.get(company_id)

        if not found_company:
            return {"error": "Company not found"}, CompanyService.NOT_FOUND

        return {
                   "company": {
                       "id": found_company.id,
                       "name": found_company.name,
                       "address": found_company.address,
                       "email": found_company.email,
                       "document": found_company.document
                   }
               }, CompanyService.OK
