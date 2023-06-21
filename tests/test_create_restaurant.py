import pytest

from app.models import Restaurant
from .fixtures import (
    app, client, tear_down_db,
    create_user, login_header
)


@pytest.mark.parametrize(
   "username, password, name, status_code, count", [
       ("ser", "12341234", "", 400, 0),
       ("ser", "12341234", None, 400, 0),
       ("ser", "12341234", "Why", 201, 1)
   ]
)
def test_create_restaurant(
    username, password, name, status_code, count,
    tear_down_db, create_user, login_header, client, app
):
    restaurant = {
        "name": name
    }

    response = client.post(
        app.url_for("routes.restaurant_create"),
        json=restaurant,
        headers=login_header
    )

    assert response.status_code == status_code
    assert Restaurant.query.count() == count
