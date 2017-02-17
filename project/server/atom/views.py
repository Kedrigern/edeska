# project/server/main/views.py


#################
#### imports ####
#################

from urllib.parse import urljoin
from flask import render_template, Blueprint, request
from werkzeug.contrib.atom import AtomFeed

from project.server import db
from project.server.models import Post

################
#### config ####
################

atom_blueprint = Blueprint('atom', __name__,)

def make_external(url):
    # TODO
    return urljoin(request.url_root, str(url))

################
#### routes ####
################

@atom_blueprint.route('/recent')
def recent():
    feed = AtomFeed('Recent Articles', feed_url=request.url, url=request.url_root)
    posts = Post.query.order_by(Post.created_at.desc()).limit(25).all()

    for post in posts:
        feed.add(post.web_title, post.content_html,
                 content_type='html',
                 author=post.author,
                 url=make_external(post.id),
                 updated=post.updated_at,
                 published=post.created_at)
    return feed.get_response()
