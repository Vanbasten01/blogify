from routes import bp
from routes.dashboard import token_required
from flask import request, render_template

@bp.route('/category', strict_slashes=False)
@token_required
def category(current_user):
    from mongo0 import categories, blogs
    category_name = request.args.get('category')

    print(f"category name   {category_name}")
  
    category = categories.find_one({"category_name": category_name})
    blog_ids = category['blogs']
    blogs_list = []
    for blog_id in blog_ids:
        blogs_list.append(blogs.find_one({'_id': blog_id}))
    return render_template('category.html', blogs=blogs_list, current_user=current_user)