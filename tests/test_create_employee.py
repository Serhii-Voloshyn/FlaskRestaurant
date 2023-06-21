import pytest

from app import models
from .fixtures import (
    app, client, tear_down_db,
    login_header, create_user, username, password
)


@pytest.mark.parametrize(
   "full_name, email, status_code, count", [
       ("", "", 400, 0),
       ("Ser", "sergmail.com", 400, 0),
       ("Ser", "ser@gmail.com", 201, 1),
   ]
)
def test_create_restaurant(
    full_name, email, status_code,
    count, tear_down_db, login_header, client, app
):
    employee = {
        "full_name": full_name,
        "email": email
    }
    response = client.post(
        app.url_for("routes.employee_create"),
        json=employee,
        headers=login_header
    )

    assert response.status_code == status_code
    assert models.Employee.query.count() == count
