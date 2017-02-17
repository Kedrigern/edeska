# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint

from project.server import db
from project.server.models import Post

################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################


@main_blueprint.route('/')
def home():
    posts = Post.query.limit(25).all()
    return render_template('main/home.html', posts=posts)

@main_blueprint.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('main/post.html', post=post)

@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")

