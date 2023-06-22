import pytest
from datetime import timedelta


from app import models
from .fixtures import (
    app, client, tear_down_db, create_restaurant,
    login_header, create_user, username, password,
    create_menu, create_vote, create_employee
)


@pytest.mark.parametrize(
   "menu_id, is_auth, status_code", [
       (0, True, 400),
       (0, False, 400),
       (1, True, 200),
       (1, False, 200),
   ]
)
def test_menu_get_vote(
    client, login_header, create_menu, 
    app, create_vote,
    menu_id, is_auth, status_code,
):

    if is_auth:
        response = client.get(
            app.url_for("routes.get_vote_by_menu", menu_id=menu_id),
            headers=login_header
        )
    else:
        response = client.get(
            app.url_for("routes.get_vote_by_menu", menu_id=menu_id),
        )
    assert response.status_code == status_code
