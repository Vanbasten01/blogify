from routes import bp
from routes.dashboard import token_required
from flask import render_template, request, flash, redirect, jsonify
from bson.objectid import ObjectId
import json

@bp.route('/delete_comment', methods=['POST'])
@token_required
def deleteComment(current_user):
    if request.method == 'POST':
        data = request.get_json()
        comment_id = data.get('comment_id')
        blog_id = request.args.get('blog_id')
        print(f"this is comment_id{comment_id} and this is {blog_id}")
        if comment_id and blog_id:
            try:
                from mongo0 import blogs
                blogs.update_one({'_id': ObjectId(blog_id)}, {'$pull': {'comments': {'comment_id': ObjectId(comment_id)}}})
                from redis0 import redis_client
                # Cache the result
                from helpers import CustomJSONEncoder
                redis_client.set('all_blogs', json.dumps(list(blogs.find().sort('_id', -1)), cls=CustomJSONEncoder))
                flash('Comment deleted successfully.', 'success')
                return jsonify({'message': 'success'}), 200
            except Exception as e:
                flash(f'An error occurred while deleting the comment: {str(e)}', 'danger')
                return jsonify({'error': 'Bad request'}), 400