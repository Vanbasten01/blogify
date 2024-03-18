from routes import bp 
from flask import session, render_template, redirect, url_for, flash, request
from bson.objectid import ObjectId
import jwt
from functools import wraps
from flask import request, jsonify
from os import getenv
from forms.searchForm import Searchform


@bp.before_request
def add_authorization_header():
    print(f" this is from befor request    {request.args.get('user_id')}")
    #if request.blueprint == 'all_routes':
    if request.args.get('user_id'):
        user_id = request.args.get('user_id')
        from mongo0 import db
        user = db.users.find_one({"_id": ObjectId(user_id)})
        print(f"this is from before request jkjkjjjjjjjjjjjjjjj{user}")
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
    if current_user is None:
        # Handle case where current_user is None (user not authenticated)
        return redirect(url_for('all_routes.login'))
    if request.method == 'POST' and form.validate_on_submit():
        keyword = form.keyword.data.lower()
        from mongo0 import blogs
        all_blogs = list(blogs.find())
        blogs = [blog for blog  in all_blogs if keyword in blog['title'].lower() or keyword in blog['content'].lower()]
        if not blogs:
            flash(f"No result Found for {keyword}", 'danger')
        return render_template('dashboard.html', current_user=current_user, blogs=all_blogs, searched_blogs=blogs, form=form)

    from mongo0 import blogs
    all_blogs = list(blogs.find())
    return render_template('dashboard.html', current_user=current_user, blogs=all_blogs, form=form)




"""
@bp.route('/dashboard/<user_id>', strict_slashes=False)
def dashboard(user_id): 

    if session['access_token']:
        if 'userinfo' in session['access_token']:
            print(session['access_token'])
            return render_template("dashboard.html", session=session.get('access_token'),
                            pretty=json.dumps(session.get("access_token"), indent=4))
        else:
            userinfo = get_user_info_from_github(session.get('access_token')['access_token'])
            if userinfo:
                return render_template('dashboard.html', session=userinfo)
    

    from mongo0 import db
    user = db.users.find_one({"_id": ObjectId(user_id)})
    print(user)

    return render_template('dashboard.html', name=user["first_name"]) """