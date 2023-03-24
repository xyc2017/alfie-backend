from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Expenses, Goals
from . import db
import json

views=Blueprint('views', __name__)

@views.route('/')
def home():
    user_expenses = []
    for expense in current_user.expenses:
        expense_data = {
            'dateOcurred': expense.dateOcurred,
            'itemName': expense.itemName,
            'price': expense.price
        }
        user_expenses.append(expense_data)
        
    user_goals = []
    for goal in current_user.goals:
        goal_data = {
            'name': goal.name,
            'description': goal.description,
            'deadline': goal.deadline
        }
        user_goals.append(goal_data)
    
    return jsonify({'expenses': user_expenses, 'goals': user_goals})
    # return render_template('home.html', user=current_user)

@views.route('/expenses', methods=['GET', 'POST'])
@login_required
def expense():
    user_expenses = []
    for expense in current_user.expenses:
        expense_data = {
            'dateOcurred': expense.dateOcurred,
            'itemName': expense.itemName,
            'price': expense.price
        }
        user_expenses.append(expense_data)
    if request.method == 'POST':
        date_occurred = request.form.get('dateOcurred')
        item_name = request.form.get('itemName')
        price = request.form.get('price')
        new_expense = Expenses(dateOcurred=date_occurred, itemName=item_name, price=price, user_id=current_user.id)
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({
            'dateOcurred': new_expense.dateOcurred,
            'itemName': new_expense.itemName,
            'price': new_expense.price,
            'user_id': new_expense.user_id
            })
    return jsonify({'expenses': user_expenses})

@views.route('/goals', methods=['GET', 'POST'])
@login_required
def goal():
    user_goals = []
    for goal in current_user.goals:
        goal_data = {
            'name': goal.name,
            'description': goal.description,
            'deadline': goal.deadline
        }
        user_goals.append(goal_data)
    if request.method == 'POST':
        goal = request.form.get('goal')
        due_date = request.form.get('dueDate')
        completed = request.form.get('completed')
        new_goal = Goals(goal=goal, dueDate=due_date, completed=completed, user_id=current_user.id)
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({
            'id': new_goal.id,
            'goal': new_goal.goal,
            'dueDate': new_goal.dueDate,
            'completed': new_goal.completed,
            'user_id': new_goal.user_id
        })
    
    #handle GET request
    return jsonify({'goals': user_goals})

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
