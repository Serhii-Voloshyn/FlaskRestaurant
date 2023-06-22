import pytest
from datetime import timedelta

from app import models
from .fixtures import (
    app, client, tear_down_db, create_restaurant,
    login_header, create_user, username, password,
    create_menu
)


@pytest.mark.parametrize(
   "is_auth, status_code", [
       (True, 200),
       (False, 200),
   ]
)
def test_menu_get_all(
    client, login_header, create_menu, app,
    is_auth, status_code
):

    if is_auth:
        response = client.get(
            app.url_for("routes.menu_get_all"),
            headers=login_header
        )
    else:
        response = client.get(
            app.url_for("routes.menu_get_all"),
        )
    assert response.status_code == status_code


@pytest.mark.parametrize(
   "is_auth, is_menu_date_exist, status_code", [
       (True, True, 200),
       (True, False, 200),
       (False, True, 200),
       (False, False, 200),
   ]
)
def test_menu_get(
    client, login_header, create_menu, app,
    is_auth, is_menu_date_exist, status_code
):
    if is_menu_date_exist:
        date = create_menu.day
    else:
        date = create_menu.day + timedelta(days=5)

    if is_auth:
        response = client.get(
            app.url_for("routes.menu_get_by_day", day=date),
            headers=login_header
        )
    else:
        response = client.get(
            app.url_for("routes.menu_get_by_day", day=date),
        )
    assert response.status_code == status_code
