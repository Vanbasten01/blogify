from routes import bp
from flask import render_template, request
from routes.dashboard import token_required
from bson.objectid import ObjectId

@bp.route('/blogs', strict_slashes=False)
@token_required
def myblogs(current_user):
    from mongo0 import blogs
    user_id = request.args.get('user_id')
    blogs = blogs.find({'user_id': ObjectId(user_id)})
    blogs = list(blogs)
    return render_template('blogs.html', blogs=blogs, current_user=current_user)