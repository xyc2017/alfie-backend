from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Expenses, Goals
from . import db
import json

views=Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method=='POST':
        dateOcurred=request.form.get('dateOcurred')
        itemName=request.form.get('itemName')
        price=request.form.get('price')
        new_expense=Expenses(dateOcurred=dateOcurred, itemName=itemName, price=price, user_id=current_user.id)
        db.session.add(new_expense)
        db.session.commit()
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_expense():
    expense=json.loads(request.data)
    expenseId=expense['expenseId']
    expense=Expenses.query.get(expenseId)
    if expense:
        if expense.user_id == current_user.id:
            db.session.delete(expense)
            db.session.commit()
    return jsonify({})