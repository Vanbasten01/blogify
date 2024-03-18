from routes import bp
from flask import render_template, request
from bson.objectid import ObjectId
from routes.dashboard import token_required



@bp.route('/blog_', strict_slashes=False)
@token_required
def Blog(current_user):
    blog_id = request.args.get("blog_id")
    user_id = request.args.get("user_id")
    from mongo0 import blogs, users
    blog_id = ObjectId(blog_id)
    blog = blogs.find_one({'_id': blog_id})
    if user_id:
        current_user = users.find_one({'_id': ObjectId(user_id)})
        return render_template('blog.html', blog=blog, current_user=current_user)

    print(f"this from specified blog {blog}")
    return render_template('blog.html', blog=blog, current_user=current_user)
