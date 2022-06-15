from flask import Flask, render_template, redirect, session, url_for, request
from splitwise import Splitwise
from splitwise.group import Group
from splitwise.user import User
from splitwise.expense import Expense
from splitwise.user import ExpenseUser
import config as Config

app = Flask(__name__)
app.secret_key = "test_secret_key"


@app.route("/")
def home():
    if 'access_token' in session:
        return redirect(url_for("dashboard"))
    return render_template("home.html")


@app.route("/login")
def login():
    sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    return redirect(url)


@app.route("/authorize")
def authorize():

    if 'secret' not in session:
        return redirect(url_for("home"))

    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
    access_token = sObj.getAccessToken(
        oauth_token, session['secret'], oauth_verifier)
    session['access_token'] = access_token

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    if 'access_token' not in session:
        return redirect(url_for("home"))

    sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
    sObj.setAccessToken(session['access_token'])
    groups = sObj.getGroups()

    return render_template("dashboard.html", groups=groups)


@app.route("/new_group")
def new_group():
    if 'access_token' not in session:
        return redirect(url_for("home"))

    sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
    sObj.setAccessToken(session['access_token'])

    friends = sObj.getFriends()

    frnz = ['Michael', 'Moin']
    user_id = {}
    for friend in friends:
        if friend.getFirstName() in frnz:
            user_id[friend.getId()] = sObj.getUser(friend.getId())

    # new code
    # create group
    users = user_id.values()
    group = Group()
    group.setName("Poker 6/14")

    group.setMembers(users)

    group, errors = sObj.createGroup(group)

    group_info = {'Name': group.getName(), 'ID': group.getId(
    ), 'Members': group.getMembers(), 'Debt': group.getSimplifiedDebts()}

    return render_template("group.html", **group_info)


@app.route("/group/<group_id>")
def group(group_id):
    if 'access_token' not in session:
        return redirect(url_for("home"))

    sObj = Splitwise(Config.consumer_key, Config.consumer_secret)
    sObj.setAccessToken(session['access_token'])

    group = sObj.getGroup(group_id)

    debts = group.getSimplifiedDebts()
    final_debts = []
    for debt in debts:
        from_user = debt.getFromUser()
        from_user = sObj.getUser(from_user)
        to_user = debt.getToUser()
        to_user = sObj.getUser(to_user)
        amount = debt.getAmount()
        final_debts.append(
            [from_user.getFirstName(), to_user.getFirstName(), amount])

    group_info = {'Name': group.getName(), 'ID': group.getId(
    ), 'Members': group.getMembers(), 'Debts': final_debts}

    return render_template("group.html", **group_info)


@app.route("/friends")
def friends():
    if 'access_token' not in session:
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
