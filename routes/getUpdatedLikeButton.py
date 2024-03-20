from routes import bp
from flask import render_template, request
from bson.objectid import ObjectId
from routes.dashboard import token_required


@bp.route('/getUpdatedLikeButton', methods=['GET'])
@token_required
def get_updated_like_button(current_user):
    blog_id = request.args.get('blog_id')
    
    # Fetch the blog from the database
    from mongo0 import blogs
    blog = blogs.find_one({'_id': ObjectId(blog_id)})
    
    if blog:
        # If the blog exists, retrieve the likes count
        blog_likes = blog.get('likes', [])
        blog_likes_count = len(blog_likes)
    else:
        # If the blog does not exist, set the likes count to 0
        blog_likes_count = 0

    # Render the template with the likes count
    updated_like_button_html = render_template('updated_like_button.html', blog_likes_count=blog_likes_count, blog=blog, current_user=current_user)
    return updated_like_button_html
