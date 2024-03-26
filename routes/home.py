from routes import bp
from functools import wraps
from flask import render_template
import json
from redis0 import redis_client



def cache_redis(key):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if the data is already cached
            cached_data = redis_client.get(key)
            if cached_data:
                print('this is from redis')
                # If data is cached, return the rendered template with the cached blog data
                return render_template('home.html', blogs=json.loads(cached_data))
            else:
                # If data is not cached, call the original function
                result = func(*args, **kwargs)
                # Cache the result
                from helpers import CustomJSONEncoder
                redis_client.set('all_blogs', json.dumps(all_blogs, cls=CustomJSONEncoder))    
                # Return the result of the original function call
                return render_template('home.html', blogs=result)
        return wrapper
    return decorator


@bp.route('/', methods=['GET'])
@cache_redis('all_blogs')
def index():
    from mongo0 import blogs
    all_blogs = list(blogs.find().sort('_id', 1))
    return all_blogs
