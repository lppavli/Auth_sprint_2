import click
from flask import Blueprint

from db.db import db
from models import User, Role
from models.db_models import UserRole

bp = Blueprint("superuser", __name__)


@bp.cli.command("create")
@click.argument("login")
@click.argument("email")
@click.argument("password")
def createsuperuser(login, email, password):
    user_exist = (
        db.session.query(User)
        .filter((User.login == login) | (User.email == email))
        .first()
    )
    if user_exist:
        return "User already exist. Try another login"
    superuser = User(login=login, is_superuser=True)
    superuser.set_password(password)
    db.session.add(superuser)
    db.session.commit()
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    new_role_user = UserRole(user_id=superuser.id, role_id=role.id)
    db.session.add(new_role_user)
    db.session.commit()
    click.echo("Superuser successfully created.")
