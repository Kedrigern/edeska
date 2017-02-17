# project/server/models.py


import datetime
import smtplib
from email.message import EmailMessage
from markdown import Markdown

from project.server import app, db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        )
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    author = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.Integer, nullable=False, default=0)
    region = db.Column(db.Integer, nullable=False, default=0)

    web_title = db.Column(db.String(255), nullable=False)
    twitter_title = db.Column(db.String(116), nullable=False)
    content_md = db.Column(db.Text(), nullable=False)
    content_html = db.Column(db.Text(), nullable=False)

    date_from = db.Column(db.DateTime)
    date_to = db.Column(db.DateTime)

    deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, title, content, author):
        self.web_title = title
        self.twitter_title = title[0:116]
        self.set_content(content)
        self.author = author
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at

    def set_content(self, content):
        self.content_md = content
        md = Markdown(extensions=['markdown.extensions.meta'])
        self.content_html = md.convert(content)

    def __repr__(self):
        return '<Post {0}>'.format(self.title)

class Template(db.Model):

    __tablename__ = "templates"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    updated_at = db.Column(db.DateTime, nullable=False)

    priority = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.Integer, nullable=False, default=0)

    name = db.Column(db.String(255), nullable=False)
    web_title = db.Column(db.String(255), nullable=False)
    twitter_title = db.Column(db.String(116), nullable=False)
    content_md = db.Column(db.String(255), nullable=False)
    content_html = db.Column(db.String(255), nullable=False)


    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at

    def __repr__(self):
        return '<Template {0}>'.format(self.title)

class Notification():

    def send(self, post):
        pass

class MailNotification(Notification):

    def send(self, post):
        msg = EmailMessage()
        msg['from'] = app.config['MAIL_FROM']
        msg['to'] = self.get_recipients()
        msg['subject'] = post.title
        msg.set_content(post.content)
        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.login(app.config['MAIL_USER'], app.config['MAIL_PASSWD'])
        server.send(msg)

    def get_recipients(self):
        return ['ondrej.profant@pirati.cz']
