from http import HTTPStatus

from flask import url_for


def test_create_role(app_with_db, login_super_user):
    response = app_with_db.post(
        url_for("roles.create_role"), json={"name": "user"}, headers=login_super_user
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json["msg"] == "Role was created"


def test_delete_role(app_with_db, login_super_user, create_role):
    response = app_with_db.delete(
        url_for("roles.delete_role", role_id=create_role), headers=login_super_user
    )
    assert response.status_code == HTTPStatus.OK


def test_roles_list(app_with_db, login_super_user, create_role):
    response = app_with_db.get(url_for("roles.roles_list"), headers=login_super_user)
    assert response.status_code == HTTPStatus.OK


def test_update_role(app_with_db, login_super_user, create_role):
    response = app_with_db.patch(
        url_for("roles.update_role", role_id=create_role),
        json={"name": "user1"},
        headers=login_super_user,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["name"] == "user1"
