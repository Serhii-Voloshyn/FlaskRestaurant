import pytest

from app.models import User
from tests.fixtures import app, client, tear_down_db


@pytest.mark.parametrize(
   "username, email, full_name, password, status_code, count", [
       ("", "", "", "", 400, 0),
       ("", "ser@gmail.com", "ser", "12341234", 400, 0),
       ("username", "", "ser", "12341234", 400, 0),
       ("username1", "ser@gmail.com", "", "12341234", 201, 1),
       ("username", "ser@gmail.com", "ser", "", 400, 0),
       ("username", "ser", "ser", "12341234", 400, 0),
       ("username", "ser", "ser", "1234", 400, 0),
       ("username2", "ser@gmail.com", "ser", "12341234", 201, 1),
   ]
)
def test_create_user(
    username, email, full_name, password,
    status_code, count, tear_down_db, client
):
    test_user = {
        "username": username,
        "email": email,
        "full_name": full_name,
        "password": password
    }
    response = client.post(
        "/api/user_create",
        json=test_user,
    )

    assert response.status_code == status_code

    assert User.query.count() == count
