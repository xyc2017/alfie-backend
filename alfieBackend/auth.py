from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from .models import User

from werkzeug.security import generate_password_hash, check_password_hash
from .app import db
from flask_login import login_user, login_required, logout_user, current_user

auth=Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    email=request.form.get('email')
    password=request.form.get('password')
    user=User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            response = {
                'status': 'success',
                'message': 'Logged in successfully!'
            }
        else:
            response = {
                'status': 'error',
                'message': 'Incorrect password. Try again.'
            }
    else:
        response = {
            'status': 'error',
            'message': 'Email does not exist'
        }
    return jsonify(response)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email=request.form.get('email')
        first_name=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        
        user=User.query.filter_by(email=email).first()
        if user:
            return jsonify({"error": "email already exists"})
        
        if len(email) < 4:
            return jsonify({"error": "email must be greater than 4 characters"})
        
        elif len(first_name) < 2:
            return jsonify({"error": "first name must be greater than 2 characters"})
    
        elif password1 != password2:
            return jsonify({"error": "passwords don\'t match"})
    
        elif len(password1) < 7:
            return jsonify({"error": "password must be greater thsn 6 characters"})
    
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')
            login_user(new_user, remember=True)
            return jsonify({"id":"new_user.id", "email":"new_user.email"})
            # return redirect(url_for('views.home')
    return jsonify({"error": "Invalid request method"}, 405)       
 