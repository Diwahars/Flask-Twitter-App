from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TwitterSearchForm(FlaskForm):
    twitter_handle = StringField('Twitter_handle', validators=[DataRequired()])
    submit = SubmitField('Search')