# from flask import Blueprint, request, redirect, url_for, session, jsonify, make_response
# from .models import User
# from .app import db
# from datetime import datetime, timedelta
# # from flask_login import login_user, login_required, logout_user, current_user
# import jwt
# from flask_bcrypt import Bcrypt
# from functools import wraps

# auth=Blueprint('auth', __name__)

# # -------------------------------------------

# @auth.route('/login', methods=['POST'])
# def login():
#     # Get the user credentials from the request
#     email = request.json.get('email')
#     password = request.json.get('password')

#     # Query the database for the user
#     user = User.query.filter_by(email=email).first()
#     print(user)
#     # Check if the password is correct
#     if user:
#         # and check_password_hash(user.password, password)
#         # Create the access token with additional claims
#         access_token = jwt.encode({"identity":user.id}, "secret", algorithm="HS256")

#         # Return the access token
#         return jsonify({'access_token': access_token}), 200

#     # Return a 401 Unauthorized if the credentials are invalid
#     return jsonify({'msg': 'Invalid email or password'}), 401

# @auth.route('/logout')
# # @jwt_required
# # .eJwlzjsOwjAMANC7ZGZwYieOe5nK8UewtnRC3J1K7G94n7LnEeezbO_jikfZX162UsMyE1UHeNfGVMHBxDXJvSl1tCacigk8HOrUNkNkgrIbrKFhyLFcCaqLQWch8rqaM8Kcdjtxc121QUh2w04zZSJVX5hc7sh1xvHftPL9ATgiMEg.ZCN1SA.Qe27fqouyaSvSyO6NZASvT-h-HE
# def logout():
#     # unset_jwt_cookies()
#     response=make_response("Cookie Removed")
#     response.set_cookie("session", "", max_age=0)
#     return jsonify({'status': 'success', 'message': 'Logged out successfully!'}), 200

# @auth.route('/signup', methods=['POST'])
# def signup():
#     data = request.get_json()
#     email = data.get('email')
#     first_name = data.get('firstName')
#     password1 = data.get('password1')
#     password2 = data.get('password2')
        
#     user = User.query.filter_by(email=email).first()
#     if user:
#         return jsonify({"error": "email already exists"}), 400
        
#     if len(email) < 4:
#         return jsonify({"error": "email must be greater than 4 characters"}), 400
        
#     elif len(first_name) < 2:
#         return jsonify({"error": "first name must be greater than 2 characters"}), 400
    
#     elif password1 != password2:
#         return jsonify({"error": "passwords don\'t match"}), 400
    
#     elif len(password1) < 7:
#         return jsonify({"error": "password must be greater than 6 characters"}), 400
    
#     else:
#         new_user = User(email=email, first_name=first_name, password=password1)
#             #             bcrpyt.generate_password_hash(
#             # password1))
#         db.session.add(new_user)
#         db.session.commit()
#         access_token = jwt.encode({"identity":new_user.id}, "secret", algorithm="HS256")
#         return jsonify({"access_token": access_token}), 200