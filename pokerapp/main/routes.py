from flask import render_template, redirect, session, url_for, flash
from flask.blueprints import Blueprint

from splitwise.group import Group
from splitwise.user import User

from pokerapp.main.util import init_obj, buy_in
from pokerapp.main.forms import NewGameForm
from pokerapp.config import BANK_ID

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


@main.route("/new_group", methods=["GET", "POST"])
def new_group():
    if 'access_token' not in session:
        return redirect(url_for("main.home"))

    form = NewGameForm()
    sObj = init_obj()

    friends = sObj.getFriends()
    form.members.choices = [(friend.getId(), friend.getFirstName())
                            for friend in friends]

    if form.validate_on_submit():
        # new code
        # create group
        group = Group()

        # group attributes
        # name
        group.setName(form.name.data)
        bank = sObj.getUser(BANK_ID)

        # members
        users = []
        for id in form.members.data:
            users.append(sObj.getUser(id))
        group.setMembers(users)

        group, errors = sObj.createGroup(group)


        # buy-in expense
        _ = buy_in(form.members.data+[sObj.getCurrentUser().getId()], form.buy_in.data, group.getId(), sObj)
        
        group_info = {'Name': group.getName(), 'ID': group.getId(
        ), 'Members': group.getMembers(), 'Debt': group.getSimplifiedDebts()}

        flash("Your game has been created!", "success")
        return render_template("main/group.html", **group_info)
    return render_template("main/create_game.html", form=form)


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


@main.route("/group/<group_id>/buy_in")
def create_expense(group_id):
    # buy-in expense
    expense = Expense()
    expense.setCost('10')
    expense.setDescription('Buy-In')
    expense.setGroupId(group_id)

    bank = ExpenseUser()
    bank.setId(sObj.getCurrentUser().getId())
    bank.setPaidShare(str((len(users))*form.buy_in.data))
    bank.setOwedShare(str((len(users))*form.buy_in.data))

    exp_users = []
    for id in form.members.data:
        exp_user = ExpenseUser()
        exp_user.setId(id)
        exp_user.setPaidShare('0.00')
        exp_user.setOwedShare(str(form.buy_in.data))
        exp_users.append(exp_user)

    expense.setUsers(exp_users)
    expense, errors = sObj.createExpense(expense)
    return redirect(url_for("main.dashboard"))
