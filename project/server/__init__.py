# project/server/__init__.py


#################
#### imports ####
#################

import os

from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api
from flask_pagedown import PageDown

################
#### config ####
################

app = Flask(
    __name__,
    template_folder='../client/templates',
    static_folder='../client/static'
)


app_settings = os.getenv('APP_SETTINGS', 'project.server.config.DevelopmentConfig')
app.config.from_object(app_settings)


####################
#### extensions ####
####################

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
toolbar = DebugToolbarExtension(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
api = Api(app)
pagedown = PageDown(app)

###################
### blueprints ####
###################

from project.server.user.views import user_blueprint
from project.server.main.views import main_blueprint
from project.server.atom.views import atom_blueprint
from project.server.admin.views import admin_blueprint
app.register_blueprint(user_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(atom_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


#####################
#### flask-login ####
#####################

from project.server.models import User

login_manager.login_view = "user.login"
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

##################
#### REST API ####
##################

from project.server.rest.v1 import PostAPI, PostListAPI

api.add_resource(PostListAPI, '/api/v1/post/', endpoint = 'posts')
api.add_resource(PostAPI, '/api/v1/post/<int:id>', endpoint = 'post')


########################
#### error handlers ####
########################

@app.errorhandler(401)
def forbidden_page(error):
    return render_template("errors/401.html"), 401


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
