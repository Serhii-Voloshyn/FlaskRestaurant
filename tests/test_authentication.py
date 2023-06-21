import pytest

from .fixtures import client, tear_down_db, create_user, app


# Username is needed for the create_user fixture,
# login_username -- data for a login request
@pytest.mark.parametrize(
   "username, login_username, password, status_code", [
       ("", "", "", 400),
       ("username", "username", "1234", 400),
       ("username", "username2", "12341235", 400),
       ("username", "username", "12341235", 200),
   ]
)
def test_login_user(
    login_username, tear_down_db, username,
    password, status_code, create_user, app, client
):
    login = {
        "username": login_username,
        "password": create_user["password"]
    }

    response = client.post(
        app.url_for("routes.login"),
        json=login,
    )
    data = response.json

    assert response.status_code == status_code

    if status_code == 200:
        assert "token" in data.keys()
        assert data["token"] is not None

    if status_code == 400:
        assert data is None
