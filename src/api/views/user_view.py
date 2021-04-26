from flask import Blueprint, request

from src.middleware.company_routes import company_routes
from src.api.services.user_service import UserService
from src.api.validators.user_validator import UserValidator
from src.middleware.private_route import private_route

user_view = Blueprint("user_view", __name__, url_prefix="/users")


@user_view.route("/", methods=["POST"])
@UserValidator.create_validator
def create_user():
    body = request.get_json()

    return UserService.create(body)


@user_view.route("/", methods=["GET"])
@company_routes
def all_users():
    user_filter = request.args.get("name")

    return UserService.list_all(user_filter)


@user_view.route("/<int:user_id>", methods=["GET"])
@company_routes
def get_user(user_id):
    return UserService.get(user_id)


@user_view.route("/<int:user_id>", methods=["PATCH", "PUT"])
@private_route
def update_user(user_id):
    # O mais importante, pois aqui que vamos atualizar o vaccine_card!!
    body = request.get_json()

    return UserService.update(body, user_id)


@user_view.route("/<int:user_id>", methods=["DELETE"])
@private_route
def delete_user(user_id):
    return UserService.delete(user_id)


@user_view.route('/login', methods=['POST'])
@UserValidator.login_validator
def login_user():
    user = request.get_json()

    return UserService.login(user['email'], user['password'])
