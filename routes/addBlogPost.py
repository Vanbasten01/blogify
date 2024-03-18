from routes import bp
from flask import render_template, request, flash, redirect, url_for, current_app
from forms.addPostForm import AddPost
from bson.objectid import ObjectId
from routes.dashboard import token_required
from werkzeug.utils import secure_filename
import os





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
       image_path = None
       if image_file:
          image_filename = secure_filename(image_file.filename)
          image_path = os.path.join(current_app.root_path, 'static', 'images', image_filename)
          image_file.save(image_path)
       user_id = current_user['_id']
       image_url = '/static/images' + image_filename if image_file  else ""       
       from mongo0 import blogs, categories

        # Check if the category already exists
       existing_category = categories.find_one({"category_name": category})
       if existing_category:
          category_id = existing_category['_id']
       else:
            # Generate a unique identifier for the category
            category_id = ObjectId()
            categories.insert_one({"_id": category_id, "category_name": category, "blogs": []})

       blog_data = {
          "title": title,
          "content": content,
          "category": category_id,
          "category_name": category,
          "image_url": image_url,
          "user_id": user_id,
          "author": current_user['first_name'] + " " + current_user["last_name"] if current_user["last_name"] else ""
       }

       insert_result = blogs.insert_one(blog_data)
       inserted_id = insert_result.inserted_id
       # Update the category document to include the new blog ID
       categories.update_one({"_id": category_id}, {"$push": {"blogs": inserted_id}})


      
       
       
       flash('Blog Added successfully', 'success')
       return redirect(url_for('all_routes.dashboard', user_id=current_user['_id']) )


       
       
   
    from mongo0 import users
    #current_user = users.find_one({"_id": ObjectId(user_id)})

    if request.method == 'POST':
      pass
    return render_template('addPost.html', current_user=current_user, form=form)
