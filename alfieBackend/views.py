from flask import Blueprint, request, session, jsonify, abort
from flask_login import login_required, current_user
from .models import Expenses, Goals
from .app import db
import json
import os
import openai
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")


views=Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
# @login_required
def home():
    expenses = Expenses.query.all()
    expenses_list = []

    for expense in expenses:
        expense_dict = {
            'id': expense.id,
            'dateOcurred': expense.dateOcurred.strftime('%m/%d/%Y'),
            'itemName': expense.itemName,
            'price': expense.price
        }
        expenses_list.append(expense_dict)
        
    goals = Goals.query.all()
    goals_list=[]
    
    for goal in goals:
        goal_dict={
            'id': goal.id,
            'goal': goal.goal,
            'dueDate': goal.dueDate,
            'completed': goal.completed
        }
        goals_list.append(goal_dict)
    
    # input_text = request.json['input']

    # Make a request to the OpenAI API
    # response = requests.post(
    #     'https://api.openai.com/v1/engines/davinci-codex/completions',
    #     headers={
    #         'Authorization': 'Bearer YOUR_API_KEY',
    #         'Content-Type': 'application/json'
    #     },
    #     json={
    #         'prompt': input_text,
    #         'max_tokens': 50,
    #         'n': 1,
    #         'stop': ['\n'],
    #         'temperature': 0.5
    #     }
    # )

    # output_text = response.json()['choices'][0]['text']

    return jsonify(expenses=expenses_list, goals=goals_list)

@views.route('/expenses', methods=['GET', 'POST'])
# @login_required
def expenses():
    expenses = Expenses.query.all()
    expenses_list = []

    for expense in expenses:
        expense_dict = {
            'id': expense.id,
            'dateOcurred': expense.dateOcurred.strftime('%m/%d/%Y'),
            'itemName': expense.itemName,
            'price': expense.price
        }
        expenses_list.append(expense_dict)
    # user_expenses = []
    # for expense in current_user.expenses:
    #     expense_data = {
    #         'dateOcurred': expense.dateOcurred,
    #         'itemName': expense.itemName,
    #         'price': expense.price
    #     }
    #     user_expenses.append(expense_data)
    if request.method == 'POST':
        date_occurred = request.form.get('dateOcurred')
        item_name = request.form.get('itemName')
        price = float(request.form.get('price'))
        new_expense = Expenses(dateOcurred=date_occurred, itemName=item_name, price=price)
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({
            'dateOcurred': new_expense.dateOcurred,
            'itemName': new_expense.itemName,
            'price': new_expense.price,
            'id': new_expense.id
            }), 201

    return jsonify({'expenses': expenses_list})

@views.route('/goals', methods=['GET', 'POST'])
# @login_required
def goals():
    goals=Goals.query.all()
    goals_list=[]
    
    for goal in goals:
        goal_dict={
            'id': goal.id,
            'goal': goal.goal,
            'dueDate': goal.dueDate,
            'completed': goal.completed
        }
        goals_list.append(goal_dict)
    # user_goals = []
    # for goal in current_user.goals:
    #     goal_data = {
    #         'name': goal.name,
    #         'description': goal.description,
    #         'deadline': goal.deadline
    #     }
    #     user_goals.append(goal_data)
    if request.method == 'POST':
        goal = request.form.get('goal')
        due_date = request.form.get('dueDate')
        completed = request.form.get('completed')
        new_goal = Goals(goal=goal, dueDate=due_date, completed=completed)
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({
            'id': new_goal.id,
            'goal': new_goal.goal,
            'dueDate': new_goal.dueDate,
            'completed': new_goal.completed,
        })
    
    return jsonify({'goals': goals_list})


@views.route('/delete-expense', methods=['DELETE'])
def delete_expense():
    expense_data = json.loads(request.data)
    expense_id = expense_data['expenseId']
    expense = Expenses.query.get(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully'})
    

@views.route('/delete-goal', methods=['DELETE'])
def delete_goal():
    goal=json.loads(request.data)
    goalId=goal['goalId']
    goal=Goals.query.get(goalId)
    db.session.delete(goal)
    db.session.commit()
    return jsonify({'message': 'Goal deleted successfully'})

@views.route('/goals/<int:goal_id>', methods=['GET'])
# @login_required
def goal(goal_id):
    goal = Goals.query.get_or_404(goal_id)
    # if goal.user_id != current_user.id:
    #     abort(403)
    # goal.goal = request.json.get('goal', goal.goal)
    # goal.dueDate = request.json.get('dueDate', goal.dueDate)
    # goal.completed = request.json.get('completed', goal.completed)
    # db.session.commit()
    return jsonify({
        'id': goal.id,
        'goal': goal.goal,
        'dueDate': goal.dueDate,
        'completed': goal.completed,
        # 'user_id': goal.user_id
    })
    
@views.route('/goals/<int:goal_id>/edit', methods=['PUT'])
# @login_required
def edit_goal(goal_id):
    goal = Goals.query.get_or_404(goal_id)
    # if goal.user_id != current_user.id:
    #     abort(403)
    goal.goal = request.json.get('goal', goal.goal)
    goal.dueDate = request.json.get('dueDate', goal.dueDate)
    goal.completed = request.json.get('completed', goal.completed)
    db.session.commit()
    return jsonify({
        'id': goal.id,
        'goal': goal.goal,
        'dueDate': goal.dueDate,
        'completed': goal.completed,
        # 'user_id': goal.user_id
    })
    
@views.route('/expenses/<int:expense_id>/edit', methods=['PUT'])
# @login_required
def edit_expense(expense_id):
    expense = Expenses.query.get_or_404(expense_id)

    if request.method == 'PUT':
        expense.dateOcurred = request.form.get('dateOcurred')
        expense.itemName = request.form.get('itemName')
        expense.price = request.form.get('price')
        db.session.commit()
        return jsonify({
            'id': expense.id,
            'dateOcurred': expense.dateOcurred,
            'itemName': expense.itemName,
            'price': expense.price,
            # 'user_id': expense.user_id
        })
        
@views.route('/expenses/<int:expense_id>', methods=['GET'])
# @login_required
def expense(expense_id):
    expense = Expenses.query.get_or_404(expense_id)

    return jsonify({
        'dateOcurred': expense.dateOcurred,
        'itemName': expense.itemName,
        'price': expense.price,
        # 'user_id': expense.user_id
    })