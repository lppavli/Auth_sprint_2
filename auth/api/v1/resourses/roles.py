from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from pydantic import UUID4

from auth.api.v1.resourses.users import jwt_roles_accepted
from auth.api.v1.schemas.roles import RoleBase
from auth.db.db import db
from auth.models.db_models import Role, User

roles = Blueprint("roles", __name__)


@roles.route("/", methods=["GET"])
@validate(response_many=True)
@jwt_required()
@jwt_roles_accepted(User, "admin")
def roles_list():
    return [RoleBase(id=role.id, name=role.name) for role in Role.query.all()]


@roles.route("/create", methods=["POST"])
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def create_role(body: RoleBase):
    role_exist = db.session.query(Role).filter(Role.name == body.name).first()
    if role_exist:
        return {"msg": "Role already exist"}, HTTPStatus.CONFLICT
    new_role = Role(name=body.name)
    db.session.add(new_role)
    db.session.commit()
    return {"msg": "Role was created"}, HTTPStatus.CREATED


@roles.route("/<role_id>", methods=["PATCH"])
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def update_role(role_id: UUID4, body: RoleBase):
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND
    name_exist = Role.query.filter_by(name=body.name).first()
    if name_exist:
        return {"msg": "Role with this name already exist"}, HTTPStatus.CONFLICT
    role.name = body.name
    db.session.query(Role).filter_by(id=role.id).update({"name": role.name})
    db.session.commit()
    return RoleBase(id=role.id, name=role.name)


@roles.route("/<role_id>", methods=["DELETE"])
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def delete_role(role_id: UUID4):
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND
    db.session.query(Role).filter_by(id=role.id).delete()
    db.session.commit()
    return {"msg": "Role succefully deleted"}, HTTPStatus.OK
