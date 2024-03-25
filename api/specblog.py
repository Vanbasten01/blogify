from bson import ObjectId
from json.decoder import JSONDecodeError
from jwt import DecodeError
from flask import request, jsonify
import json
import jwt
from os import getenv
from mongo0 import db  
from redis0 import redis_client 
from . import bp_api 

@bp_api.route('/api/blogs/<blog_id>', strict_slashes=False)
def blog(blog_id):
    token = request.headers.get('x-token')
 
    if token:
        blog = None
        blog_id = str(blog_id)
        print(f"this is /api/blogs/blog_id   {token}")
        try:
            print(f"this is /api/blogs/blog_id   {token}")
            data = jwt.decode(token, getenv('FLASK_SECRET'), algorithms=['HS256'])
            email = data.get('email')
            if redis_client.get(email):
                print(f"this is /api/blogs/blog_id   {token}")
                all_blogs_json = redis_client.get('all_blogs')
                if all_blogs_json:
                    all_blogs = json.loads(all_blogs_json)
                    for blog in all_blogs:
                        if blog['_id'] == blog_id:
                            print(f"this is fromm rediiiiiiiiiiiiiiiiis")
                            return jsonify(blog), 200
                blog = db.blogs.find_one({'_id': ObjectId(blog_id)})
                if not blog:
                    return jsonify({'message': 'Blog not found'}), 404
        except DecodeError:
            return jsonify({'error': 'invalid token'}), 401
        except JSONDecodeError:
            return jsonify({'error': 'invalid JSON in Redis'}), 500
    else:
        return jsonify({'error': 'Token not provided'}), 401
