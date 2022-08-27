from flask import url_for, request

from auth.models.db_models import UserHistory
from http import HTTPStatus


def test_auth_user(app_with_db, user):
    response = app_with_db.post(
        url_for("auth.login_user"), json={"login": "sergio", "password": "pass"}
    )
    assert response.status_code == HTTPStatus.OK


def test_auth_unknown_user(app_with_db, user):
    response = app_with_db.post(
        url_for("auth.login_user"), json={"login": "joe", "password": "pass"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_user(app_with_db):
    response = app_with_db.post(
        url_for("auth.create_user"), json={"login": "John", "password": "Abcdefgh"}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json["msg"] == "User was created."


def test_get_user_history(app_with_db, user, access_token):
    user_id = str(user.id)
    user_agent = request.headers.get("user-agent", "")
    user_host = request.headers.get("host", "")
    user_info = UserHistory(
        user_id=user_id,
        user_agent=user_agent,
        ip_address=user_host,
    )
    response = app_with_db.get(url_for("auth.get_history"), headers=access_token)
    assert response.status_code == HTTPStatus.OK


def test_logout(app_with_db, access_token):
    response = app_with_db.delete(url_for("auth.logout"), headers=access_token)
    assert response.status == "200 OK"
    assert response.json["msg"] == "Access token revoked"


def test_change_password(app_with_db, user, access_token):
    response = app_with_db.patch(
        url_for("auth.change_password"),
        json={"old_password": "pass", "new_password": "news"},
        headers=access_token,
    )
    assert response.status == "200 OK"
    assert response.json["msg"] == "Password changed successfully"


def test_refresh(app_with_db, user, refresh_token):
    response = app_with_db.post(url_for("auth.refresh_token"), headers=refresh_token)
    assert response.status == "200 OK"
