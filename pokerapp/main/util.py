from flask import session, flash

from splitwise import Splitwise
from splitwise.group import Group
from splitwise.expense import Expense
from splitwise.user import ExpenseUser

from pokerapp.config import CONSUMER_KEY, CONSUMER_SECRET, BANK_ID


def init_obj():
    sObj = Splitwise(CONSUMER_KEY, CONSUMER_SECRET)
    sObj.setAccessToken(session['access_token'])
    return sObj


def create_group():
    group = Group()

    # group attributes
    # name
    group.setName(form.name.data)

    # members
    users = []
    for id in form.members.data:
        users.append(sObj.getUser(id))
    group.setMembers(users)

    group, errors = sObj.createGroup(group)
    return True


def buy_in(players, amount, group_id, sObj):
    # buy-in expense
    expense = Expense()
    expense.setCost(str((len(players))*amount))
    expense.setDescription('Buy-In')
    expense.setGroupId(group_id)

    bank = ExpenseUser()
    bank.setId(BANK_ID)
    bank.setPaidShare(str((len(players))*amount))
    bank.setOwedShare('0')

    exp_users = [bank]
    for id in players:
        exp_user = ExpenseUser()
        exp_user.setId(id)
        exp_user.setPaidShare('0.00')
        exp_user.setOwedShare(str(amount))
        exp_users.append(exp_user)

    expense.setUsers(exp_users)
    expense, errors = sObj.createExpense(expense)
    if errors:
        print(errors.getErrors())
        flash("Something is fucking wrong and we will fix it.")
        return False
    else:
        return True
