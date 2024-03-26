from routes import bp
from flask import render_template, request, flash, jsonify
from bson.objectid import ObjectId
from routes.dashboard import token_required
from forms.commentForm import CommentForm
from uuid import uuid4
from datetime import datetime



@bp.route('/blog_', methods=['GET', 'POST'], strict_slashes=False)
@token_required
def Blog(current_user):
    form = CommentForm()
    blog_id = request.args.get("blog_id")
    user_id = request.args.get("user_id")
    print(f"welcome to the blog_ 6666666")
    if request.method == 'POST' and form.validate_on_submit():
        try:
            from mongo0 import blogs
            print(f"welcome to the blog_ 99999999")
            blog = blogs.find_one({'_id': ObjectId(blog_id)})
            if 'comments' not in blog:
                blogs.update_one({'_id': blog_id}, {'$set': {'comments': []}})
            comment = form.comment.data
            # Get the current date and time
            current_time = datetime.now()
            current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"here we go comment i just added {comment}")
            comment_id = ObjectId()
            blogs.update_one({'_id': ObjectId(blog_id)}, {'$push': {'comments': {'comment_id': comment_id, 'user_id': ObjectId(user_id), 'likes': [], 'comment': comment, 'date': current_time }}})
            from redis0 import redis_client
            # Cache the result
            from helpers import CustomJSONEncoder
            redis_client.set('all_blogs', json.dumps(list(blogs.find()), cls=CustomJSONEncoder))

            flash('Your comment has been added.', 'success')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

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
            'likes': '$comments.likes',
            'time': '$comments.time'
        }}
    ])

 
    comments = []
    for c in comments_with_users:
       comments.append(c)
    

   
    from mongo0 import blogs
    blog_id = ObjectId(blog_id)
    blog = blogs.find_one({'_id': blog_id})
   

    return render_template('blog.html', blog=blog, current_user=current_user, form=form, comments=comments)

