from flask import render_template, redirect, session, url_for, flash
from flask.blueprints import Blueprint

from splitwise.group import Group
from splitwise.user import User
from splitwise.expense import Expense
from splitwise.user import ExpenseUser

from pokerapp.main.util import init_obj

main = Blueprint('main', __name__, template_folder='templates',
                 static_folder='static', static_url_path='/main/static')


@main.route("/")
def home():
    if 'access_token' in session:
        return redirect(url_for("main.dashboard"))
    return render_template("main/home.html")


@main.route("/dashboard")
def dashboard():
    if 'access_token' not in session:
        return redirect(url_for("main.home"))

    sObj = init_obj()
    groups = sObj.getGroups()

    return render_template("main/dashboard.html", groups=groups)


@main.route("/new_group")
def new_group():
    if 'access_token' not in session:
        return redirect(url_for("main.home"))

    sObj = init_obj()

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

    return render_template("main/group.html", **group_info)


@main.route("/group/<group_id>")
def group(group_id):
    if 'access_token' not in session:
        return redirect(url_for("main.home"))

    sObj = init_obj()

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

    return render_template("main/group.html", **group_info)


@main.route("/group/<group_id>/delete")
def delete_group(group_id):
    if 'access_token' not in session:
        return redirect(url_for("main.home"))

    sObj = init_obj()

    sObj.deleteGroup(group_id)
    flash("Group deleted successfully", 'success')

    return redirect(url_for("main.dashboard"))
