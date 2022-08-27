from http import HTTPStatus

from flask import url_for


def test_assign_roles(app_with_db, user, login_super_user, create_role):
    response = app_with_db.post(
        url_for("users.assign_roles"),
        json={"user_id": user.id, "role_id": create_role},
        headers=login_super_user,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json["msg"] == "Role is assigned to the user"


def test_delete_role_from_user(app_with_db, assign_role, login_super_user):
    response = app_with_db.delete(
        url_for("users.delete_role_from_user"),
        json={"user_id": assign_role["user_id"], "role_id": assign_role["role_id"]},
        headers=login_super_user,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["msg"] == "Role for user succefully deleted"


def test_user_roles(app_with_db, user, access_token):
    response = app_with_db.get(url_for("users.get_user_roles"), headers=access_token)
    assert response.status_code == HTTPStatus.OK
