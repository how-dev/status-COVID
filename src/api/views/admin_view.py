from flask import Blueprint, request

from src.api.validators.admin_validator import AdminValidator
from src.api.services.admin_service import AdminService

from src.middleware.admin_routes import admin_routes

admin_view = Blueprint("admin_view", __name__, url_prefix="/admin")


@admin_view.route('/login', methods=['POST'])
@AdminValidator.login_validator
def login_user():
    admin = request.get_json()

    return AdminService.login(admin['email'], admin['password'])


@admin_view.route('/', methods=['POST'])
@admin_routes
def create_admin():
    body = request.get_json()

    return AdminService.create(body)
