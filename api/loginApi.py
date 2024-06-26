#from app import app
from flask import jsonify, redirect, url_for, request, flash, make_response
from forms.loginForm import LoginForm
from . import bp_api
import bcrypt
from os import getenv
import jwt
from bson.objectid import ObjectId
from datetime import timedelta



@bp_api.route('/api/login', methods=['POST'])
def login():
    if request.method == "POST":
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        from mongo0 import db
        user = db.users.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Generate JWT token
            token = jwt.encode({'email': email}, getenv('FLASK_SECRET'), algorithm='HS256')
            from redis0 import redis_client
            redis_client.setex(email, timedelta(hours=6), token)
            
            # Set token in the response headers
            headers = {"Authorization": f"Bearer {token}"}
            
            # Return success response with token
            response = make_response({'message': 'You have logged in successfully'})
            response.headers = headers
            return response
        else:
            # Return error response if authentication fails
            return jsonify({'error': 'Invalid credentials'}), 401