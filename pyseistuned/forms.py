#!/usr/bin/env python

"""
Copyright 2020, Benjamin L. Dowdell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[
        Email(message=('Not a valid email address.')),
        DataRequired()
    ])
    body = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=4, message=('Please enter a longer message.'))
    ])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
