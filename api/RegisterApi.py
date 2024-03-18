from . import bp_api
from flask import jsonify, request
import bcrypt
import re

MIN_PASSWORD_LENGTH = 8

# Regular expression pattern for email validation
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

# Define your Flask API route
@bp_api.route('/api/signup', methods=['POST'])
def api_signup():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Validate email format using regex
        if not re.match(EMAIL_REGEX, email):
            return jsonify({'error': 'Invalid email address'}), 400

        # Password length validation
        if len(password) < MIN_PASSWORD_LENGTH:
            return jsonify({'error': f'Password must be at least {MIN_PASSWORD_LENGTH} characters long'}), 400

        # Password match validation
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400

        # Additional password complexity validation
        if not (any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in '@$!%*?&' for c in password)):
            return jsonify({'error': 'Password must contain uppercase, lowercase, number, and special character.'}), 400

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Construct user data
        user_data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": hashed_password.decode('utf-8')
        }

        # Insert the user data into the database
        from mongo0 import users
        users.insert_one(user_data)

        return jsonify({'message': 'Account created successfully'}), 201

    return "Welcome to Blogify"