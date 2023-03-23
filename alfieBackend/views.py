from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Expenses, Goals
from . import db
import json

views=Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/expenses', methods=['GET', 'POST'])
@login_required
def expense():
    if request.method=='POST':
        dateOcurred=request.form.get('dateOcurred')
        itemName=request.form.get('itemName')
        price=request.form.get('price')
        new_expense=Expenses(dateOcurred=dateOcurred, itemName=itemName, price=price, user_id=current_user.id)
        db.session.add(new_expense)
        db.session.commit()
    return render_template("expenses.html", user=current_user)

@views.route('/delete-expense', methods=['POST'])
def delete_expense():
    expense=json.loads(request.data)
    expenseId=expense['expenseId']
    expense=Expenses.query.get(expenseId)
    if expense:
        if expense.user_id == current_user.id:
            db.session.delete(expense)
            db.session.commit()
    return jsonify({})

@views.route('/goals', method=['GET', 'POST'])
@login_required
def goal():
    if request.method=='POST':
        goal=request.form.get('goal')
        dueDate=request.form.get('dueDate')
        completed=request.form.get('completed')
        new_goal=Goals(goal=goal, dueDate=dueDate, completed=completed, user_id=current_user.id)
        db.session.add(new_goal)
        db.session.commit()
    return render_template("goals.html", user=current_user)

@views.route('/delete-goal', methods=['POST'])
def delete_goal():
    goal=json.loads(request.data)
    goalId=goal['goalId']
    goal=Goals.query.get(goalId)
    if goal:
        if goal.user_id==current_user.id:
            db.session.delete(goal)
            db.session.commit()
    return jsonify({})
