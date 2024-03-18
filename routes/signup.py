
from routes import bp
from mongo0 import users
from flask import render_template, redirect, url_for, request, flash
import bcrypt

@bp.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    from forms.registrationForm import RegistrationForm
    form = RegistrationForm(request.form)


    if request.method == 'POST' and form.validate_on_submit():
        # Process form data
        #from app import users
       
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": hashed_password.decode('utf-8'),
            "profile_image": ""
        }
        
        users.insert_one(user_data)
        flash('Account created successfully', 'success')
        
        # Redirect to a success page or do something with the data
        return redirect(url_for('all_routes.index'))
    return render_template('signup.html', form=form)

    