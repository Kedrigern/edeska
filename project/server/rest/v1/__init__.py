# project/server/rest/v1/__init__.py

import json
from flask.ext.restful import Resource, reqparse
from flask_restful import fields, marshal, marshal_with

from project.server.models import Post
from project.server import db

fields_get = {'id': fields.Integer,
         'title_web': fields.Raw, 'title_twitter': fields.Raw,
         'content_md': fields.Raw, 'content_html': fields.Raw,
         'author': fields.Raw,
         'created_at': fields.DateTime, 'updated_at': fields.DateTime}

class PostListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('priority')
        self.reqparse.add_argument('category')
        self.reqparse.add_argument('title', type = str, location = 'json', help= 'Post title')
        self.reqparse.add_argument('content_md', type = str, location = 'json', help= 'Post content in markdown' )
        self.reqparse.add_argument('content_html', type = str, location = 'json', help= 'Post content in HTML' )
        self.reqparse.add_argument('author', type = str, location = 'json')
        super(PostListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        my_q = Post.query
        if args['priority'] and not args['priority'] == 0:
            my_q = my_q.filter_by(priority=args['priority'])
        if args['category'] and not args['category'] == 0:
            my_q = my_q.filter_by(category=args['category'])
        posts = my_q.limit(25).all()
        return {'posts': [marshal(post, fields_get) for post in posts]}

    def post(self):
        args = self.reqparse.parse_args()
        db.session.add(Post(args['title'], args['content'], args['author']))
        db.session.commit()
        return {'post': marshal(Post, fields_get)}, 201


class PostAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json', help= 'Post title')
        self.reqparse.add_argument('content_html', type = str, location = 'json', help= 'Post content in HTML' )
        self.reqparse.add_argument('content_md', type = str, location = 'json', help= 'Post content in markdown' )
        self.reqparse.add_argument('author', type = str, location = 'json')
        super(PostAPI, self).__init__()

    @marshal_with(fields_get)
    def get(self, id):
        return Post.query.get_or_404(id)

    def put(self, id):
        args = self.reqparse.parse_args()
        post = Post.query.get_or_404(id)
        for k, v in args.items():
            if v is not None:
                post[k] = v
        db.commit()
        return {'post': marshal(Post, fields_get)}, 201

    def delete(self, id):
        post = Post.query.get_or_404(id)
        post.deleted = True
        db.commit()
        return {'result': True}

