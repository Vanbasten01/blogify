from routes import bp 
from flask import session, render_template, redirect, url_for, flash, request
from bson.objectid import ObjectId
import jwt
from functools import wraps
from flask import request, jsonify
from os import getenv
from forms.searchForm import Searchform
import json


@bp.before_request
def add_authorization_header():
    if request.args.get('user_id'):
        user_id = request.args.get('user_id')
        from mongo0 import db
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return redirect(url_for('all_routes.login'))
        token = session.get(user['email'])
      
        # Create a copy of the headers and modify the copy
        headers = dict(request.headers)
        headers['Authorization'] = f'Bearer {token}'
        # Update the request headers with the modified copy
        request.headers = headers
   
      




def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(f"this is from wrapper {token}")
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
           

        # Check if the token starts with 'Bearer '
        if 'Bearer ' not in token:
            return jsonify({'message': 'Invalid token format'}), 401

        token = token.split(' ')[1]  # Extract the token after 'Bearer '

        try:
            data = jwt.decode(token, getenv('FLASK_SECRET'), algorithms=['HS256'])
            from mongo0 import users
            current_user = users.find_one({"email": data['email']})
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired'}), 401
        except jwt.InvalidTokenError:
            #return jsonify({'message': 'Invalid token'}), 401
             return redirect(url_for('all_routes.login'))
        # Pass the current_user and other arguments to the protected route
        return f(current_user, *args, **kwargs)

    return decorated_function

@bp.route('/dashboard/', methods=['GET', 'POST'])
@token_required
def dashboard(current_user):
    form = Searchform()
    from redis0 import redis_client
    from mongo0 import blogs
    if current_user is None:
        # Handle case where current_user is None (user not authenticated)
        return redirect(url_for('all_routes.login'))
    if request.method == 'POST' and form.validate_on_submit():
        keyword = form.keyword.data.lower()
        
        all_blogs = json.loads(redis_client.get('all_blogs'))
        blogs = [blog for blog  in all_blogs if keyword in blog['title'].lower() or keyword in blog['content'].lower()]
        if not blogs:
            flash(f"No result Found for {keyword}", 'danger')
        return render_template('dashboard.html', current_user=current_user, blogs=all_blogs, searched_blogs=blogs, form=form)

    
    all_blogs = json.loads(redis_client.get('all_blogs'))
    return render_template('dashboard.html', current_user=current_user, blogs=all_blogs, form=form)