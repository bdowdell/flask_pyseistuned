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

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, DecimalField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[
        Email(message='Not a valid email address.'),
        DataRequired()
    ])
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=4, message='Please enter a longer message.')
    ])
    submit = SubmitField('Submit')


class TuningWedgeForm(FlaskForm):
    """Inputs for calculating tuning wedge"""
    layer_1_vp = IntegerField('vp_1')
    layer_1_dens = DecimalField('rho_1')
    layer_2_vp = IntegerField('vp_2')
    layer_2_dens = DecimalField('rho_2')
    layer_3_vp = IntegerField('vp_3')
    layer_3_dens = DecimalField('rho_3')
    vp_units = RadioField(label='Vp Units', choices=[(0, 'm/s'), (1, 'ft/s')])
    wv_type = SelectField(label='Wavelet', choices=[(0, 'Ricker'), (1, 'Ormsby')])
    frequency = IntegerField('Frequency (Hz)')
    wv_length = DecimalField('Length (s)', places=3)
    wv_dt = DecimalField('dt (s)', places=3)
    submit = SubmitField('Calculate')
