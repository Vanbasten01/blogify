from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import cloudinary
from dotenv import load_dotenv
from os import getenv
import uuid
#from bson.json_util import dumps
#import json
from authlib.integrations.flask_client import OAuth
from flask_swagger_ui import get_swaggerui_blueprint
from flask_ckeditor import CKEditor






load_dotenv()

app = Flask(__name__)

#intiantiate a ckeditor instance
ckeditor = CKEditor(app)


          
cloudinary.config( 
  cloud_name = getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key = getenv("CLOUDINARY_API_KEY"), 
  api_secret = getenv("CLOUDINARY_API_SECRET")
)

### swagger specific ###
SWAGGER_URL = '/api/'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Blogify"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
from api import bp_api as api_routes
app.register_blueprint(api_routes)
### end swagger specific ###


oauth = OAuth(app)

oauth = OAuth(app)
oauth.register("myApp",
               client_id=getenv("OAUTH2_CLIENT_ID"),
               client_secret=getenv("OAUTH2_CLIENT_SECRET"),
               server_metadata_url=getenv("OAUTH2_META_URL"),
               client_kwargs={"scope": "openid email profile"}
               )
oauth.register("github",
               client_id=getenv("GITHUB_CLIENT_ID"),
               client_secret=getenv("GITHUB_CLIENT_SECRET"),
               authorize_url="https://github.com/login/oauth/authorize",
               authorize_params=None,
               access_token_url="https://github.com/login/oauth/access_token",
               access_token_params=None,
               refresh_token_url=None,
               client_kwargs={"scope": "user:email"}
               )

app.secret_key = getenv("FLASK_SECRET")



#app.config['SECRET_KEY'] = getenv("FLASK_SECRET")
from routes import bp as all_routes

@all_routes.route("/githubLogin")
def githubLogin():
    return oauth.github.authorize_redirect(redirect_uri=url_for('all_routes.callbackgithub', _external=True))

@all_routes.route("/callback/github", strict_slashes=False)
def callbackgithub():
    token = oauth.github.authorize_access_token()
   
    # session['access_token'] = token
    from helpers import get_user_info_from_github
    userinfo = get_user_info_from_github(token.get('access_token'))
    from mongo0 import db 
    user = db.users.find_one({'github_id': userinfo.get('id') })
    if user:
        import jwt
        token = jwt.encode({'email': user['email']}, getenv('FLASK_SECRET'), algorithm='HS256')
        session[user['email']] = token
        return redirect(url_for('all_routes.dashboard', user_id=user['_id']))

    name = userinfo.get('name')
    email = f"user{str(uuid.uuid4())}@example.com"
    user_data = {
            "email": email,
            "first_name": name,
            "last_name": None,
            "password": None,
            "github_id": userinfo.get('id')
        }
    import jwt
    token = jwt.encode({'email': email}, getenv('FLASK_SECRET'), algorithm='HS256')
    from mongo0 import db 
    user = db.users.find_one({'github_id': userinfo.get('id') })
    print(f"this is form user mongo db  {user}")
    result = db.users.insert_one(user_data)
    inserted_id = result.inserted_id
    session[user_data.get('email')] = token
    return redirect(url_for('all_routes.dashboard', user_id=str(inserted_id)))
       
    


@all_routes.route("/googleLogin")
def googleLogin():
    return oauth.myApp.authorize_redirect(redirect_uri=url_for('all_routes.callback', _external=True))


@all_routes.route("/callback", strict_slashes=False)
def callback():
    google_token = oauth.myApp.authorize_access_token()
    print(f"thiss iss from gooogle      {google_token}")
    name = google_token['userinfo']['name']
    email = google_token['userinfo']['email']
    user_data = {
            "email": email,
            "first_name": name,
            "last_name": None,
            "password": None,
            "profile_image": None
        }
    import jwt
    token = jwt.encode({'email': email}, getenv('FLASK_SECRET'), algorithm='HS256')
    session[email] = token
    from mongo0 import db    
    user = db.users.insert_one(user_data)
    #inserted_id = result.inserted_id
    inserted_id = user.inserted_id
    return redirect(url_for('all_routes.dashboard', user_id=str(inserted_id)))




app.register_blueprint(all_routes)


if __name__ == "__main__":
    app.run(debug=True)
