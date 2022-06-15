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
        return redirect(url_for("friends"))
    return render_template("home.html")

@app.route("/login")
def login():

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    return redirect(url)


@app.route("/authorize")
def authorize():

    if 'secret' not in session:
        return redirect(url_for("home"))

    oauth_token    = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    access_token = sObj.getAccessToken(oauth_token,session['secret'],oauth_verifier)
    session['access_token'] = access_token

    return redirect(url_for("friends"))


@app.route("/friends")
def friends():
    if 'access_token' not in session:
        return redirect(url_for("home"))

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    sObj.setAccessToken(session['access_token'])

    friends = sObj.getFriends()

    for friend in friends:
        if friend.getFirstName() == "Moin":
            moinID = friend.getId()
        elif friend.getFirstName() == "Amy":
            amyID = friend.getId()

    # new code
    # create group
    group = Group()
    group.setName("Testing")

    user1 = sObj.getUser(moinID)

    user2 = sObj.getUser(amyID)

    user3 = sObj.getCurrentUser()

    users = []
    users.append(user1)
    users.append(user2)
    users.append(user3)

    group.setMembers(users)

    group, errors = sObj.createGroup(group)
    groupId = group.getId()

    expense = Expense()
    expense.setCost('10')

    user1 = ExpenseUser()
    user1.setId(moinID)
    user1.setPaidShare('10.00')
    user1.setOwedShare('2.0')

    user2 = ExpenseUser()
    user2.setId(amyID)
    user2.setPaidShare('5.00')
    user2.setOwedShare('8.00')

    user3 = ExpenseUser()
    user3.setId(user3.getId())
    user3.setPaidShare('5.00')
    user3.setOwedShare('10.00')
    expense.setDescription("Testing")
    expense.setGroupId(groupId)


    expense.setUsers(users)

    expense, errors = sObj.createExpense(expense)

    return render_template("friends.html",friends=friends)




if __name__ == "__main__":
    app.run(threaded=True,debug=True)
