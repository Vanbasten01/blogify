# routes/__init__.py
from flask import Blueprint

bp = Blueprint('all_routes', __name__)
from routes.home import index
from routes.login import login
from routes.signup import signup
from routes.dashboard import dashboard
from routes.addBlogPost import addPost
from routes.specBlog import blog
from routes.profile import profile
from routes.blogs import myblogs
from routes.deleteBlog import delete_blog
from routes.editBlog import edit_Blog
from routes.category import category
from routes.blog import Blog




