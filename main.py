import asyncio
from flask import Flask, send_file, make_response, request
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from util.badge_loader import load_badges 
from util.html_to_png import html_to_png

# Load environment variables
load_dotenv()
env = os.getenv('ENV', 'development')
debug = env == 'development'

# Setup Flask
app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour",
                    "10 per minute", "4 per second"],
    storage_uri="memory://",
)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Load badges
badges = load_badges()

@app.route('/')
@cache.cached(timeout=1000, query_string=True)
def index():
    return "Guide Placeholder" # TODO: Add simple guide to the API

@app.route('/<badge>/<owner>/<repo>', methods=['GET'])
@cache.cached(timeout=60 * 3, query_string=True)
def home(badge, owner, repo):
    # Find the badge from badges where the id property matches the badge variable
    badge = next((b for b in badges if b.id == badge), None)
    if not badge:
        return "Badge not found", 404
    
    badge_html = badge.create(owner, repo, request.args)
    badge_png = asyncio.run(html_to_png(badge_html))

    mimetype = 'image/png'
    response = make_response(
        send_file(badge_png, mimetype=mimetype))
    
    response.headers['Content-Type'] = mimetype
    response.headers['Cache-Control'] = f'public, max-age={60 * 3}'
    response.headers['Expires'] = f'{60 * 3}'
    
    return response


if __name__ == '__main__':
    app.run(debug=debug)
