from routes import bp
from flask import render_template, request, redirect, url_for
from routes.dashboard import token_required
from bson.objectid import ObjectId

@bp.route('/delete_blog', strict_slashes=False)
@token_required
def delete_blog(current_user):
    blog_id = request.args.get('blog_id')
    from mongo0 import blogs, categories

    blog = blogs.find_one({'_id': ObjectId(blog_id)})
    category_name = blog['category_name']
    

    # Use the $pull operator to remove the specified blog ID from the category
    categories.update_one({'category_name': category_name}, {'$pull': {'blogs': ObjectId(blog_id)}})
  
    blogs.delete_one({'_id': ObjectId(blog_id)})
    return redirect(url_for('all_routes.myblogs', user_id=current_user['_id']))

