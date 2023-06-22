import pytest

from app import models
from .fixtures import (
    app, client, tear_down_db, create_restaurant,
    login_header, create_user, username, password,
    create_menu, create_employees
)


@pytest.mark.parametrize(
   "menu_id, employee_id, score, status_code, count", [
       (2, 1, 5, 400, 0),
       (1, 3, 5, 400, 0),
       (1, 1, 6, 400, 0),
       (1, 1, 0, 400, 0),
       (1, 1, 2.5, 400, 0),
       (1, 1, 1, 201, 1),
       (1, 1, 5, 201, 1),
   ]
)
def test_create_vote_authorized(
    status_code, count, app,
    tear_down_db, login_header, client,
    create_menu, create_employees,
    menu_id, employee_id, score
):
    vote = {
        "menu_id": menu_id,
        "employee_id": employee_id,
        "score": score
    }

    response = client.post(
        app.url_for("routes.create_vote"),
        json=vote,
        headers=login_header
    )

    assert response.status_code == status_code
    assert models.Vote.query.count() == count


@pytest.mark.parametrize(
   "menu_id, employee_id, score", [
       (2, 1, 5),
       (1, 3, 5),
       (1, 1, 6),
       (1, 1, 0),
       (1, 1, 2.5),
       (1, 1, 1),
       (1, 1, 5),
   ]
)
def test_create_vote_unauthorized(
    app, tear_down_db, client,
    create_menu, create_employees,
    menu_id, employee_id, score
):
    vote = {
        "menu_id": menu_id,
        "employee_id": employee_id,
        "score": score
    }

    response = client.post(
        app.url_for("routes.create_vote"),
        json=vote,
    )

    assert response.status_code == 401
    assert models.Vote.query.count() == 0


def test_create_vote_authorized_employee_dublicate(
    app, tear_down_db, login_header, client,
    create_menu, create_employees,
):
    vote = {
        "menu_id": 1,
        "employee_id": 1,
        "score": 5
    }

    response = client.post(
        app.url_for("routes.create_vote"),
        json=vote,
        headers=login_header
    )

    assert response.status_code == 201
    assert models.Vote.query.count() == 1

    response = client.post(
        app.url_for("routes.create_vote"),
        json=vote,
        headers=login_header
    )

    assert response.status_code == 400
    assert models.Vote.query.count() == 1
