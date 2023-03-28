from flask import Blueprint, request, session, jsonify, abort
from flask_login import login_required, current_user
from .models import Expenses, Goals
import openai
from .app import db
import json

views=Blueprint('views', __name__)


@views.route('/', methods=['POST'])
@login_required
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
    
    request_json = request.get_json()
    prompt = request_json['prompt']
    
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    generated_text = response.choices[0].text.strip()
    
    return jsonify({'expenses': user_expenses, 'goals': user_goals, 'generated_text': generated_text})

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

@views.route('/goals/<int:goal_id>', methods=['PUT'])
@login_required
def update_goal(goal_id):
    goal = Goals.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        abort(403)
    goal.goal = request.json.get('goal', goal.goal)
    goal.dueDate = request.json.get('dueDate', goal.dueDate)
    goal.completed = request.json.get('completed', goal.completed)
    db.session.commit()
    return jsonify({
        'id': goal.id,
        'goal': goal.goal,
        'dueDate': goal.dueDate,
        'completed': goal.completed,
        'user_id': goal.user_id
    })
@views.route('/expenses/<int:expense_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expenses.query.get_or_404(expense_id)

    if request.method == 'POST':
        expense.dateOcurred = request.form.get('dateOcurred')
        expense.itemName = request.form.get('itemName')
        expense.price = request.form.get('price')
        db.session.commit()
        return jsonify({
            'dateOcurred': expense.dateOcurred,
            'itemName': expense.itemName,
            'price': expense.price,
            'user_id': expense.user_id
        })
        
