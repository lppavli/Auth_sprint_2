from http import HTTPStatus
from functools import wraps
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate

from auth.api.v1.schemas.roles import RoleUser, RoleBase
from auth.db.db import db
from auth.models.db_models import UserRole, User

users = Blueprint("users", __name__)


def jwt_roles_accepted(model, *roles: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            user_id = get_jwt_identity()
            user = model.query.filter_by(id=user_id).first()
            if not user or not user.roles:
                return {"msg": "Доступ запрещен."}, HTTPStatus.PAYMENT_REQUIRED

            user_roles = set(role.name for role in user.roles)
            if not user_roles.intersection(roles):
                return {"msg": "Доступ запрещен."}, HTTPStatus.PAYMENT_REQUIRED
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


@users.route("/roles", methods=["GET"])
@validate(response_many=True)
@jwt_required()
def get_user_roles():
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    if user is None:
        return {"message": "User not found. Check uuid"}
    return [RoleBase(name=role.name) for role in user.roles]


@users.route("/assign-roles", methods=["POST"])
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def assign_roles(body: RoleUser):
    role_user_exist = (
        db.session.query(UserRole)
        .filter(UserRole.user_id == body.user_id, UserRole.role_id == body.role_id)
        .first()
    )
    if role_user_exist:
        return {"msg": "Role is already assigned to the user"}, HTTPStatus.CONFLICT
    new_role_user = UserRole(user_id=body.user_id, role_id=body.role_id)
    db.session.add(new_role_user)
    db.session.commit()
    return {"msg": "Role is assigned to the user"}, HTTPStatus.CREATED


@users.route("/delete_role", methods=["DELETE"])
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def delete_role_from_user(body: RoleUser):
    role_user = (
        db.session.query(UserRole)
        .filter(UserRole.user_id == body.user_id, UserRole.role_id == body.role_id)
        .first()
    )
    if not role_user:
        return {"msg": "Role for user not found"}, HTTPStatus.NOT_FOUND
    db.session.query(UserRole).filter_by(
        user_id=body.user_id, role_id=body.role_id
    ).delete()
    db.session.commit()
    return {"msg": "Role for user succefully deleted"}, HTTPStatus.OK
