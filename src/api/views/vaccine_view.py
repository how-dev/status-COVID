from flask import Blueprint, request

from src.api.services.vaccine_service import VaccineService
from src.middleware.private_route import private_route
from src.middleware.admin_routes import admin_routes
from src.middleware.company_routes import company_routes

vaccine_view = Blueprint("vaccine_view", __name__, url_prefix="/vaccine")


@vaccine_view.route("/", methods=["POST"])
@private_route
def new_vaccine():
    body = request.get_json()

    return VaccineService.create(body)


@vaccine_view.route("/<int:user_id>", methods=["GET"])
@company_routes
def get_all_vaccines(user_id):
    return VaccineService.list_all(user_id)


@vaccine_view.route("/<int:vaccine_id>", methods=["PATCH", "PUT"])
@admin_routes
def update_vaccine(vaccine_id):
    body = request.get_json()
    return VaccineService.update(body, vaccine_id)
