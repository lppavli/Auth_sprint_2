import uuid
from datetime import datetime

from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class UserRole(db.Model):
    __tablename__ = "users_roles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id"),
        default=uuid.uuid4(),
        nullable=False,
    )
    role_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("roles.id"),
        default=uuid.uuid4(),
        nullable=False,
    )


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, unique=False, default=False)
    roles = db.relationship("Role", secondary="users_roles", back_populates="users")

    def __repr__(self):
        return f"<User {self.login}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self

    def check_password(self, password):
        return check_password_hash(self.password, password)


def create_partition(target, connection, **kw) -> None:
    """creating partition by user_sign_in"""
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_smart" PARTITION OF "users_sign_in" FOR VALUES IN ('smart')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_mobile" PARTITION OF "users_sign_in" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_web" PARTITION OF "users_sign_in" FOR VALUES IN ('web')"""
    )


class SocialAccount(db.Model):
    __tablename__ = "social_account"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(User, backref=db.backref("social_accounts", lazy=True))

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    # __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'),)

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    name = db.Column(db.String(32), unique=True, nullable=False)
    users = db.relationship("User", secondary="users_roles", back_populates="roles")

    def __repr__(self):
        return f"<Role {self.name}>"


class UserHistory(db.Model):
    """Модель для истории входов в аккаунт пользователя"""

    __tablename__ = "user_history"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    user_agent = db.Column(db.String, nullable=True)
    ip_address = db.Column(db.String, nullable=True)
    auth_datetime = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"UserHistory: {self.user_agent} - {self.auth_datetime}"
