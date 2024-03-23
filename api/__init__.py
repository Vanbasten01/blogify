from flask import Blueprint

bp_api = Blueprint('api_routes',__name__)
from api.RegisterApi import api_signup
from api.loginApi import login
from api.blogs import blogs