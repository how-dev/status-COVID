from flask import Blueprint, request

from src.api.services.test_service import TestService
from src.middleware.private_route import private_route
from src.middleware.admin_routes import admin_routes
from src.middleware.company_routes import company_routes

test_view = Blueprint('test_view', __name__, url_prefix='/tests')


@test_view.route('/<int:user_id>', methods=['GET'])
@company_routes
def list_user_tests(user_id):
    return TestService.list_all(user_id)


@test_view.route('/user/<int:test_id>', methods=['GET'])
@company_routes
def find_test(test_id):
    return TestService.find(test_id)


@test_view.route('/', methods=['POST'])
@private_route
def create_test():
    body = request.get_json()

    return TestService.create(body)
