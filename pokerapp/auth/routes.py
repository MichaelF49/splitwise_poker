from flask import request, session, redirect, url_for
from flask.blueprints import Blueprint
from splitwise import Splitwise

from pokerapp.config import CONSUMER_KEY, CONSUMER_SECRET

auth = Blueprint('auth', __name__)


@auth.route("/login")
def login():
    sObj = Splitwise(CONSUMER_KEY, CONSUMER_SECRET)
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    return redirect(url)


@auth.route("/authorize")
def authorize():

    if 'secret' not in session:
        return redirect(url_for("main.home"))

    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    sObj = Splitwise(CONSUMER_KEY, CONSUMER_SECRET)
    access_token = sObj.getAccessToken(
        oauth_token, session['secret'], oauth_verifier)
    session['access_token'] = access_token

    return redirect(url_for("main.dashboard"))


@auth.route("/logout")
def logout():
    session.pop('access_token', None)
    session.pop('secret', None)
    return redirect(url_for("main.home"))
