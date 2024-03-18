from routes import bp
from routes.dashboard import token_required
from flask import request, render_template, current_app, flash, redirect, url_for
from forms.addPostForm import AddPost
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import os


@bp.route('/edit/blog', methods=['GET', 'POST'], strict_slashes=False)
@token_required
def edit_Blog(current_user):
    blog_id = request.args.get('blog_id')
    from mongo0 import blogs, categories
    blog = blogs.find_one({'_id': ObjectId(blog_id)})
    form = AddPost()
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        category = form.category.data
        content = form.content.data
        image_file = form.image.data
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.root_path, 'static', 'images', image_filename)
            image_file.save(image_path)
            blog_data = {
            "title": title,
            "content": content,
            "category_name": category,
            "image_url": "/static/images/" + image_filename,
            }
        else:
            blog_data = {
                "title": title,
                "content": content,
                "category_name": category,
            }
        if category != blog['category']:
            categories.update_one({'category_name': blog['category_name']}, {'$pull': {'blogs': ObjectId(blog_id)} })
            # Check if the category already exists
            existing_category = categories.find_one({"category_name": category})
            if existing_category:
                category_id = existing_category['_id']
            else:
                # Generate a unique identifier for the category
                category_id = ObjectId()
                categories.insert_one({"_id": category_id, "category_name": category, "blogs": []})
            categories.update_one({"_id": category_id}, {"$push": {"blogs": blog['_id']}})
            


        result = blogs.update_one({'_id': ObjectId(blog_id)}, {'$set': blog_data})
        if result.modified_count == 1:
            flash('Blog updated successfully', 'success')
        else:
            flash('Failed to update blog', 'error')
        return redirect(url_for('all_routes.myblogs', user_id=current_user['_id']))
    
    form.title.data = blog['title']
    form.category.data = blog['category']
    form.content.data = blog['content']
    form.image.data = blog['image_url']
    return render_template('edit_blog.html', current_user=current_user, form=form)


        







        