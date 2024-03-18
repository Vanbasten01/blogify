from routes import bp
from routes.dashboard import token_required
from flask import request, render_template
from forms.searchForm import Searchform

@bp.route('/seach', methods=['POST'], strict_slashes=False)
@token_required
def seach(current_user):
    form = Searchform()
    keyword = form.keyword.data
    blogs = []
    from mongo0 import blogs
    all_blogs = list(blogs.find())
    for blog in all_blogs:
        if keyword in blog['title'].lower() or keyword in blog['content'].lower():
            blogs.append(blog)
    if blogs:
        return render_template('search.html', blogs=blogs, current_user=current_user)
    return 
