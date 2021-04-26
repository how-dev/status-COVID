from flask import Flask
from flask.cli import AppGroup
from sqlalchemy import and_
from click import argument
from faker import Faker
from random import randint
from typing import List

from src.api.models import UserModel, VaccineModel, TestModel, CompanyModel, AdminModel


def random_boolean():
    return randint(0, 2) == 0


def cli_database(app: Flask):
    cli_group_table = AppGroup("database")

    @cli_group_table.command("drop")
    def drop_all():
        app.db.drop_all()

    @cli_group_table.command("create")
    def create_all():
        app.db.create_all()

    app.cli.add_command(cli_group_table)


def cli_company(app: Flask):
    cli_group_company = AppGroup("company")

    @cli_group_company.command("create")
    @argument("quantity")
    def cli_company_bulk_create(quantity):
        session = app.db.session
        fake = Faker()

        company_to_insert = (
            CompanyModel(
                name=fake.name(),
                email=fake.unique.email(),
                document=str(fake.unique.unix_time())[0:14] + "0",
                address=fake.address()
            )
            for _ in range(int(quantity))
        )

        for index, company in enumerate(company_to_insert):
            company.password = '123456'
            session.add(company)
            if index % 50 == 0:
                session.commit()
        session.commit()
    app.cli.add_command(cli_group_company)


def cli_admin(app: Flask):
    cli_group_admin = AppGroup("admin")

    @cli_group_admin.command("create")
    @argument("quantity")
    def cli_admin_bulk_create(quantity):
        session = app.db.session
        fake = Faker()

        admin_to_insert = (
            AdminModel(
                name=fake.name(),
                email=fake.unique.email()
            )
            for _ in range(int(quantity))
        )
        for index, admin in enumerate(admin_to_insert):
            admin.password = 'admin'
            session.add(admin)
            if index % 50 == 0:
                session.commit()
        session.commit()
    app.cli.add_command(cli_group_admin)


def cli_user(app: Flask):
    cli_group_user = AppGroup("user")

    @cli_group_user.command("create")
    @argument("quantity")
    def cli_user_bulk_create(quantity):
        session = app.db.session
        fake = Faker()

        user_to_insert = (
            UserModel(
                name=fake.name(),
                age=randint(2, 100),
                email=fake.unique.email(),
                document=str(fake.unique.unix_time())[0:11] + "0",
                live_with=randint(0, 10),
                exposed_works=random_boolean()
            )
            for _ in range(int(quantity))
        )
        for index, user in enumerate(user_to_insert):
            user.password = '123456'
            session.add(user)
            if index % 50 == 0:
                session.commit()
        session.commit()
    app.cli.add_command(cli_group_user)


def cli_vaccine(app: Flask):
    cli_group_vaccine = AppGroup("vaccine")

    @cli_group_vaccine.command("create")
    @argument("quantity", nargs=1)
    @argument("user_scope", nargs=1)
    def cli_vaccine_bulk_create(quantity, user_scope):
        fake = Faker()
        session = app.db.session
        n_range = [int(n) for n in user_scope.split("-")]
        users_in_chunck: List[UserModel] = (
            session.query(UserModel)
            .filter(and_(UserModel.id >= n_range[0], UserModel.id <= n_range[1]))
            .all()
        )
        vaccines = [
            "Tozinameran",
            "mRNA-1273",
            "CoronaVac",
            "Covishield",
            "Sputnik V",
            "Convidicea",
            "BBIBP-CorV",
            "Covaxin"
        ]

        user_vaccine_list = lambda: (
            VaccineModel(
                name=vaccines[randint(0, len(vaccines) - 1)],
                record=randint(1000, 10000),
                voucher=f"https://www.{fake.unique.name().split(' ')[0].lower()}.com.br"
            )
            for _ in range(int(quantity))
        )
        for user in users_in_chunck:
            user.vaccines = [*user.vaccines, *list(user_vaccine_list())]
            session.add(user)
            session.commit()
        session.commit()
    app.cli.add_command(cli_group_vaccine)


def cli_test(app: Flask):
    cli_group_test = AppGroup("test")

    @cli_group_test.command("create")
    @argument("quantity", nargs=1)
    @argument("user_scope", nargs=1)
    def cli_test_bulk_create(quantity, user_scope):
        fake = Faker()
        session = app.db.session

        n_range = [int(n) for n in user_scope.split("-")]

        users_in_chunck: List[UserModel] = (
            session.query(UserModel)
                .filter(and_(UserModel.id >= n_range[0], UserModel.id <= n_range[1]))
                .all()
        )

        users_tests_list = lambda: (
            TestModel(date_stamp=fake.date(), result=random_boolean())
            for _ in range(int(quantity))
        )
        for user in users_in_chunck:
            user.tests_list = [*user.tests_list, *list(users_tests_list())]
            session.add(user)
            session.commit()
        session.commit()

    app.cli.add_command(cli_group_test)


def init_app(app: Flask):
    cli_user(app)
    cli_vaccine(app)
    cli_database(app)
    cli_test(app)
    cli_company(app)
    cli_admin(app)
