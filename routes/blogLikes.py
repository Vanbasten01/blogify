from routes import bp
from routes.dashboard import token_required
from flask import request, flash, jsonify, redirect
from bson.objectid import ObjectId

@bp.route('/blogLikes', methods=['POST'])
@token_required
def bloglikes(current_user):
    blog_id = request.args.get("blog_id")
    user_id = request.args.get("user_id")

    if request.method == 'POST':
        try:
            from mongo0 import blogs

            # Check if both blog_id and user_id are valid ObjectId strings
            if not ObjectId.is_valid(blog_id) or not ObjectId.is_valid(user_id):
                raise ValueError("Invalid ObjectId")

            blog = blogs.find_one({'_id': ObjectId(blog_id)})
            if 'likes' not in blog:
                blogs.update_one({'_id': ObjectId(blog_id)}, {'$set': {'likes': []}})
                
            liked = blogs.find_one({'_id': ObjectId(blog_id), 'likes': {'$elemMatch': {'user_id': ObjectId(user_id)}}})
            liked = liked is not None
            
            if liked:
                blogs.update_one({'_id': ObjectId(blog_id)}, {'$pull': {'likes': {'user_id': ObjectId(user_id)}}})
                #flash('Comment unliked successfully.', 'success')
            else:
                blogs.update_one({'_id': ObjectId(blog_id)}, {'$push': {'likes': {'user_id': ObjectId(user_id)}}})
                #flash('Comment liked successfully.', 'success')
            
            return jsonify({'liked': liked}), 200

        except ValueError as ve:
            #flash(f'Invalid ObjectId: {str(ve)}', 'danger')
            return jsonify({'error': 'bad request'}), 400

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return jsonify({'error': 'bad request'}), 400

    return jsonify({'error': 'bad request'}), 400
