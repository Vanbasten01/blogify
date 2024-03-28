from routes import bp
from routes.dashboard import token_required
from flask import request, flash, redirect, jsonify
from bson.objectid import ObjectId
from mongo0 import blogs

@bp.route('/like_comment', methods=['POST'])
@token_required
def like_comment(current_user):
    blog_id = request.args.get('blog_id')
    user_id = request.args.get('user_id')
    
    if request.method == 'POST':
        try:
            # Retrieve comment_id from the request body
            data = request.get_json()
            comment_id = data.get('comment_id')
            print(f"comment_id:  {comment_id}")
            print(f"user_id:   {user_id}")

            comment = blogs.find_one({
                '_id': ObjectId(blog_id),
                'comments': {
                    '$elemMatch': {
                        'comment_id': ObjectId(comment_id),
                        'likes': ObjectId(user_id)
                    }
                }
            })
            liked = comment is not None
            print(f"here is liked {liked}")
            if liked:
                blogs.update_one({'_id': ObjectId(blog_id), 'comments.comment_id': ObjectId(comment_id)},
                                {'$pull': {'comments.$.likes': ObjectId(user_id)}})
                flash('Comment unliked successfully.', 'success')
            else:
                # If not liked, add the user to the likes array
                blogs.update_one({'_id': ObjectId(blog_id), 'comments.comment_id': ObjectId(comment_id)},
                                {'$push': {'comments.$.likes': ObjectId(user_id)}})
                flash('Comment liked successfully.', 'success')
            # Return a 200 response indicating success
            return jsonify({'message': 'Success'}), 200
        except Exception as e:
            flash(f'An error occurred while toggling the comment like status: {str(e)}', 'danger')

    return jsonify({'error': 'Bad request'}), 400
