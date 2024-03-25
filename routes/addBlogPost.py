from routes import bp
from flask import render_template, request, flash, redirect, url_for, current_app
from forms.addPostForm import AddPost
from bson.objectid import ObjectId
from routes.dashboard import token_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import json
import cloudinary.uploader



@bp.route('/add_Post', methods=['GET', 'POST'], strict_slashes=False)
@token_required
def addPost(current_user):
    form = AddPost()
    if request.method == 'POST' and form.validate_on_submit():
       
       title = form.title.data
       content = form.content.data
       category = form.category.data
       # Extract the image file from the form
       image_file = form.image.data
       if image_file:
          # Upload image to Cloudinary
          uploaded_image = cloudinary.uploader.upload(image_file)

          # Get the URL of the uploaded image from Cloudinary
          image_url = uploaded_image['secure_url']

       else:
            # If no image is uploaded, set image_url to None
            image_url = None
       user_id = current_user['_id']      
       from mongo0 import blogs, categories

        # Check if the category already exists
       existing_category = categories.find_one({"category_name": category})
       if existing_category:
          category_id = existing_category['_id']
       else:
            # Generate a unique identifier for the category
            category_id = ObjectId()
            categories.insert_one({"_id": category_id, "category_name": category, "blogs": []})
       current_time = datetime.now()
       current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

       blog_data = {
          "title": title,
          "content": content,
          "category": category_id,
          "category_name": category,
          "image_url": image_url,
          "user_id": user_id,
          "author": current_user['first_name'] + " " + current_user["last_name"] if current_user["last_name"] else "",
          "date": current_time
       }

       insert_result = blogs.insert_one(blog_data)
       inserted_id = insert_result.inserted_id
       # Update the category document to include the new blog ID
       categories.update_one({"_id": category_id}, {"$push": {"blogs": inserted_id}})


       from redis0 import redis_client

      

       all_blogs = list(blogs.find())
       from helpers import CustomJSONEncoder
       redis_client.set('all_blogs', json.dumps(all_blogs, cls=CustomJSONEncoder))    
       
       flash('Blog Added successfully', 'success')
       return redirect(url_for('all_routes.dashboard', user_id=current_user['_id']) )


       
    return render_template('addPost.html', current_user=current_user, form=form)
