from flask import session
from splitwise import Splitwise
from pokerapp.config import CONSUMER_KEY, CONSUMER_SECRET


def init_obj():
    sObj = Splitwise(CONSUMER_KEY, CONSUMER_SECRET)
    sObj.setAccessToken(session['access_token'])
    return sObj
