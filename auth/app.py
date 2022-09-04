import sys
from flask import Flask, request
from flask_jwt_extended import JWTManager

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from auth.api.v1.resourses.oauth import oauth
from auth.api.v1.resourses.auth import auth
from auth.api.v1.resourses.roles import roles
from auth.api.v1.resourses.users import users

from auth.db.db import init_db


# from auth.createsuperuser import bp

# https://oauth.yandex.ru/client/6d91b9f55fb64927aa474d50566c566b
def create_app():
    app = Flask(__name__)
    app.config['OAUTH_CREDENTIALS'] = {
        'google': {
            'client_id': '1010159233057-3spqffma16s74i4kgq458cvdp1rlj5iv.apps.googleusercontent.com',
            'client_secret': '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',
            'authorize_url': 'https://accounts.google.com/',
            'access_token_url': 'https://oauth2.googleapis.com/token',
            'base_url': 'https://www.googleapis.com/oauth2/v1/'
        },
        'yandex': {
            'client_id': 'f8142cc1a9c44dd0a43875e58b80f3be',
            'client_secret': '9982a0b55bd14faf8775c98da9ea1ef9',
            'authorize_url': 'https://oauth.yandex.ru/authorize',
            'access_token_url': 'https://oauth.yandex.ru/token',
            'base_url': 'https://login.yandex.ru/',
            'redirect_uri': 'https://oauth.yandex.ru/verification_code'
        },
    }
    # Swagger доступен по адресу http://127.0.0.1/apidocs/
    swagger = Swagger(app, template_file="project-description/openapi.yaml")
    jwt = JWTManager(app)
    db = SQLAlchemy(app)
    ma = Marshmallow(app)

    app.register_blueprint(auth, url_prefix="/api/v1/auth")
    app.register_blueprint(roles, url_prefix="/api/v1/roles")
    app.register_blueprint(users, url_prefix="/api/v1/users")
    app.register_blueprint(oauth, url_prefix="/api/v1/oauth")
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
