from flask import Flask


def init_app(app: Flask):
    from src.api.views.company_view import company_view
    from src.api.views.user_view import user_view
    from src.api.views.test_view import test_view
    from src.api.views.vaccine_view import vaccine_view
    from src.api.views.admin_view import admin_view

    app.register_blueprint(company_view)
    app.register_blueprint(test_view)
    app.register_blueprint(user_view)
    app.register_blueprint(admin_view)

    app.register_blueprint(vaccine_view)
