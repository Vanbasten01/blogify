from routes import bp
from flask import render_template, request
from bson.objectid import ObjectId
from routes.dashboard import token_required
from forms.commentForm import CommentForm
import json



@bp.route('/blog', strict_slashes=False)
def blog():
    form = CommentForm()
    blog_id = request.args.get("blog_id")
    blog = None
    from mongo0 import db
    from redis0 import redis_client
    all_blogs_json = redis_client.get('all_blogs')
    if all_blogs_json:
        all_blogs = json.loads(all_blogs_json)
        for blog in all_blogs:
            if blog['_id'] == blog_id:
                 blog = blog
            else:
                 blog = db.blogs.find_one({'_id': ObjectId(blog_id)})

   
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

    return render_template('blog.html', blog=blog, form=form, comments=comments)
