from routes import bp
from routes.dashboard import token_required
from flask import request, flash, session, jsonify
from bson.objectid import ObjectId

@bp.route('/delete_profile', methods=['POST'], strict_slashes=False)
@token_required
def delete_profile(current_user):
    if request.method == 'POST':
        user_id = request.args.get('user_id')
        from mongo0 import users
        deleted_user = users.delete_one({'_id': ObjectId(user_id)})
        if deleted_user.deleted_count == 1:
            session.pop(current_user['email'])
            flash('Account deleted Successfully', 'success')
            return  jsonify({'message': "account deleted successfully"}), 200
            
        else:
            flash('User not found or unable to delete', 'error')
            return  jsonify({'message': "User not found or unable to delete"}), 400

