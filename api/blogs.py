from api import bp_api
from flask import request, jsonify
import jwt
from os import getenv
from json.decoder import JSONDecodeError
from jwt import DecodeError
import json


@bp_api.route('/api/blogs', methods=['GET', 'POST'], strict_slashes=False)
def blogs():
    token = request.headers.get('x-token')
    print(f"here is the   {token}")
    if token:
        try:

            data = jwt.decode(token, getenv('FLASK_SECRET'), algorithms=['HS256'])
            email = data.get('email')
            print(f"h=thsi is email {email}")
            from redis0 import redis_client
            if redis_client.get(email):
                all_blogs_json = redis_client.get('all_blogs')
                all_blogs = json.loads(all_blogs_json)
                return jsonify(all_blogs), 200
        except DecodeError:
            return jsonify({'error': 'invalid token'}), 401
        except JSONDecodeError:
            return jsonify({'error': 'invalid JSON in Redis'}), 500
    else:
        return jsonify({'error': 'Token not provided'}), 401
            
