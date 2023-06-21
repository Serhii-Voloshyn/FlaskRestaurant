import pytest

from app import models
from .fixtures import (
    app, client, tear_down_db, create_restaurant,
    login_header, create_user, username, password
)


@pytest.mark.parametrize(
   "restaurant_id, date, status_code, count", [
       ("0", "2023-06-19", 400, 0),
       ("1", "2023-06-19-01", 400, 0),
       ("1", "2023-06-19", 201, 1)
   ]
)
def test_create_restaurant(
    restaurant_id, date, status_code, count, app,
    tear_down_db, create_restaurant, login_header, client
):
    menu = {
        "restaurant_id": restaurant_id,
        "day": date,
    }
    response = client.post(
        app.url_for("routes.menu_create"),
        json=menu,
        headers=login_header
    )

    assert response.status_code == status_code
    assert models.Menu.query.count() == count
