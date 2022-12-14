from flask import Blueprint
from auth.api.v1.resourses.oauth_helper.oauth import OAuthSignIn
from auth.db.db import db
from auth.models import User
from auth.models.db_models import SocialAccount

oauth = Blueprint("oauth_helper", __name__)


@oauth.route("/authorize/<provider>")
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@oauth.route("/callback/<provider>")
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        return {"msg": "Account not found"}
    social_acc = SocialAccount.query.filter(
        (SocialAccount.social_id == social_id) | (SocialAccount.social_name == provider)
    ).first()
    if social_acc is None:
        user = User(login=username, email=email)
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        social = SocialAccount(
            social_id=social_id,
            social_name=provider,
            user_id=str(user.id),
        )
        db.session.add(social)
        db.session.commit()
    else:
        user = social_acc.user
    return oauth.create_tokens(identity=user.id)
