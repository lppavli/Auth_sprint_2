import sys
from flask import Flask, request
from flask_jwt_extended import JWTManager

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from auth.api.v1.resourses.auth import auth
from auth.api.v1.resourses.roles import roles
from auth.api.v1.resourses.users import users

from auth.db.db import init_db
# from auth.createsuperuser import bp


def create_app():
    app = Flask(__name__)

    # Swagger доступен по адресу http://127.0.0.1/apidocs/
    swagger = Swagger(app, template_file="project-description/openapi.yaml")
    jwt = JWTManager(app)
    db = SQLAlchemy(app)
    ma = Marshmallow(app)

    app.register_blueprint(auth, url_prefix="/api/v1/auth")
    app.register_blueprint(roles, url_prefix="/api/v1/roles")
    app.register_blueprint(users, url_prefix="/api/v1/users")
    # app.register_blueprint(bp)
    init_db(app)
    return app


app = create_app()


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')


if __name__ == '__main__':
    app.run(debug=True)
