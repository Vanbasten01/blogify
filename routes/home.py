from flask import  render_template
from routes import bp


@bp.route('/', methods=['GET', 'POST'])
def index():
    from mongo0 import blogs
    all_blogs = list(blogs.find())
    return render_template('home.html', blogs=all_blogs)
   