from routes import bp
from flask import render_template, request
from bson.objectid import ObjectId
from routes.dashboard import token_required
from forms.commentForm import CommentForm



@bp.route('/blog', methods=['GET', 'POST'], strict_slashes=False)
#@token_required
#def blog(current_user):
def blog():
    form = CommentForm()
    blog_id = request.args.get("blog_id")
    from mongo0 import blogs, users
    blog_id = ObjectId(blog_id)
    blog = blogs.find_one({'_id': blog_id})
    from mongo0 import db
    # Retrieve comments with user information
    comments_with_users = db.blogs.aggregate([
        {'$match': {'_id': ObjectId(blog_id)}},
        {'$unwind': '$comments'},
        {'$lookup': {
            'from': 'users',
            'localField': 'comments.user_id',
            'foreignField': '_id',
            'as': 'comment_user'
        }},
        {'$project': {
            '_id': 0,
            'comment': '$comments.comment',
            'user_name': '$comment_user.first_name',  
            'user_id': '$comments.user_id',
            'comment_id': '$comments.comment_id',
            'time': '$comments.time'
        }}
    ])

 
    comments = []
    for c in comments_with_users:
       comments.append(c)
    comments_len = len(comments)

    return render_template('blog.html', blog=blog, form=form, comments=comments, length=comments_len) #current_user=current_user)
