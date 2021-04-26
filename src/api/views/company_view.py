from flask import Blueprint, request

from src.api.services.company_service import CompanyService
from src.middleware.admin_routes import admin_routes
from src.middleware.company_routes import company_routes

company_view = Blueprint("company_view", __name__, url_prefix="/companies")


@company_view.route("/", methods=["POST"])
def create_company():
    body = request.get_json()

    return CompanyService.create(body)


@company_view.route("/", methods=["GET"])
@admin_routes
def all_companies():
    companies_filter = request.args.get("name")

    return CompanyService.list_all(companies_filter)


@company_view.route("/<int:company_id>", methods=["GET"])
@admin_routes
def get_company(company_id):
    return CompanyService.get(company_id)


@company_view.route("/<int:company_id>", methods=["PATCH", "PUT"])
@company_routes
def update_company(company_id):

    body = request.get_json()

    return CompanyService.update(body, company_id)


@company_view.route("/<int:company_id>", methods=["DELETE"])
@company_routes
def delete_company(company_id):
    return CompanyService.delete(company_id)


@company_view.route('/login', methods=['POST'])
def login_company():
    company = request.get_json()

    return CompanyService.login(company['email'], company['password'])
