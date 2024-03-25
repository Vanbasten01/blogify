from routes import bp
from routes.dashboard import token_required
from flask import flash, redirect, render_template, request, url_for, current_app
from bson import ObjectId
from mongo0 import users
from forms.editregistration import RegistrationFormU
import bcrypt
from werkzeug.utils import secure_filename
import os
import cloudinary.uploader


@bp.route('/profile', methods=['GET', 'POST'], strict_slashes=False)
@token_required
def profile(current_user):
    user_id = request.args.get('user_id')

    if user_id is None:
        flash('User ID is required.', 'error')
        return redirect(url_for('all_routes.index'))

    user = users.find_one({ '_id': ObjectId(user_id) })

    if user is None:
        flash('User not found.', 'error')
        return redirect(url_for('all_routes.index'))

    form = RegistrationFormU()
   

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        if password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            password = hashed_password.decode('utf-8')
        else:
            password = user['password']
        # Extract the image file from the form
        image_file = request.files['profile_image']
        #image_file = form.profile_image.data
      
        if image_file:
            uploaded_image = cloudinary.uploader.upload(image_file)

            # Get the URL of the uploaded image from Cloudinary
            image_url = uploaded_image['secure_url']

            user_data = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "profile_image": image_url
            }
        else:
            user_data = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
            }

        users.update_one({'_id': user['_id']}, {'$set': user_data})
        flash('Account updated successfully', 'success')

        # Redirect to a success page or do something with the data
        return redirect(url_for('all_routes.dashboard', user_id=user['_id']))

    form.email.data = user['email']
    form.first_name.data = user['first_name']
    form.last_name.data = user['last_name']
    form.password.data = ""
    form.confirm_password.data = ""
    form.profile_image.data = user.get('profile_image', '')

    return render_template('profile.html', form=form, current_user=current_user)
