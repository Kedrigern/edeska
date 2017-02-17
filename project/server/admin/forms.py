# project/server/admin/forms.py


from flask_wtf import Form
from wtforms import TextField
from wtforms.fields.html5 import DateField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class EditForm(Form):
    web_title = TextField('Nadpis pro web', [DataRequired(), Length(min=6, max=255)])
    twitter_title = TextField('Twitter', [DataRequired(), Length(min=12, max=116)])
    content_md = PageDownField('Obsah')
    date_from = DateField('Platnost od')
    date_to = DateField('Platnost do')
