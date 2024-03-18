#from app import app
from flask import render_template, redirect, url_for, request, flash, make_response, session
from forms.loginForm import LoginForm
from routes import bp
import bcrypt
from os import getenv
import jwt
from bson.objectid import ObjectId



@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        from mongo0 import db
        user = db.users.find_one({"email": email})
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                # Generate JWT token
                token = jwt.encode({'email': email}, getenv('FLASK_SECRET'), algorithm='HS256')

                print(token)
                session[email] = token
                if request.args.get('blog_id'):
                    blog_id = request.args.get('blog_id')
                    return redirect(url_for('all_routes.blog', blog_id=blog_id, user_id=user['_id']))
                #flash('You have logged in successfully', 'success')
                return redirect(url_for('all_routes.dashboard', user_id=user['_id']))
        else:
            flash('Invalid Email or Password', 'danger')
            return redirect(url_for('all_routes.login'))
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    user_id = request.args.get('user_id')
    from mongo0 import db
    
    user = db.users.find_one({"_id": ObjectId(user_id)})
    session.pop(user['email'])
    session.clear()
    flash('See you soon!!', 'success')
    return redirect(url_for('all_routes.index'))
    
