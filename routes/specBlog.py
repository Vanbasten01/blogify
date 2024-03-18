from routes import bp
from flask import render_template, request
from bson.objectid import ObjectId
from routes.dashboard import token_required



@bp.route('/blog', strict_slashes=False)
#@token_required
#def blog(current_user):
def blog():
    blog_id = request.args.get("blog_id")
    from mongo0 import blogs, users
    blog_id = ObjectId(blog_id)
    blog = blogs.find_one({'_id': blog_id})
    print(f"this from specified blog {blog}")
    return render_template('blog.html', blog=blog) #current_user=current_user)
