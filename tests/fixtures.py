from app import create_app
from app import models
from app import db

import pytest
import datetime
from flask import current_app

from config import TestConfig


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def tear_down_db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def username():
    return "ser"


@pytest.fixture()
def password():
    return "bananas123"


@pytest.fixture()
def create_user(tear_down_db, username, password, client):
    user = {
        "username": username,
        "password": password,
        "full_name": "ser",
        "email": "ser@gmail.com"
    }
    client.post(current_app.url_for("routes.user_create"), json=user)

    return user


@pytest.fixture()
def create_restaurant(tear_down_db):
    restaurant = {
        "name": "bananas"
    }
    restaurant = models.Restaurant(**restaurant)

    tear_down_db.session.add(restaurant)
    tear_down_db.session.commit()

    return restaurant


@pytest.fixture()
def login_header(tear_down_db, create_user, client, app):
    login = {
        "username": create_user["username"],
        "password": create_user["password"]
    }
    token = client.post(
        app.url_for("routes.login"),
        json=login,
    ).json["token"]

    return {"x-access-token": f"{token}"}


@pytest.fixture()
def create_menu(create_restaurant, tear_down_db):
    menu = {
        "restaurant_id": create_restaurant.id,
        "day": datetime.datetime.strptime("2023-06-20", "%Y-%m-%d").date()
    }
    menu = models.Menu(**menu)

    tear_down_db.session.add(menu)
    tear_down_db.session.commit()

    return menu


@pytest.fixture()
def create_employee(tear_down_db):
    employee = dict(
        full_name="ser",
        email="ser@gmail.com"
    )

    employee = models.Employee(**employee)

    tear_down_db.session.add(employee)
    tear_down_db.session.commit()
    
    return employee


@pytest.fixture()
def create_vote(create_menu, create_employee, tear_down_db):
    vote = dict(
        menu_id = create_menu.id,
        employee_id = create_employee.id,
        score = 4
    )

    vote = models.Vote(**vote)

    tear_down_db.session.add(vote)
    tear_down_db.session.commit()
    
    return vote
