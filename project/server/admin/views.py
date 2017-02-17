# project/server/admin/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask.ext.login import  login_required
from wtforms import TextField
from wtforms.ext.sqlalchemy.orm import model_form
from flask_pagedown.fields import PageDownField

from project.server import bcrypt, db
from project.server.models import Post
from project.server.admin.forms import EditForm
from flask_wtf import Form

################
#### config ####
################

admin_blueprint = Blueprint('admin', __name__,)

@admin_blueprint.route('/dashboard')
@login_required
def dashboard():
    posts = Post.query.all()
    return render_template('admin/dashboard.html', posts=posts)

@admin_blueprint.route('/edit/<int:id>')
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    exclude = ['content_html', 'created_at', 'updated_at']
    field_args = {'content_md': {'label': 'text'}}
    PostForm = model_form(Post, base_class=Form, exclude=exclude, field_args=field_args)
    form = PostForm(obj=post)
    #if form.validate_on_submit():
    #    content = form.content.data
    #    pass
    return render_template('admin/edit.html', post=post, form=form)

#field_args={
##    'content_md': {'widget': PageDownField()},
#    }
