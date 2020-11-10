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
from wtforms.validators import ValidationError, DataRequired, Email, Length, NumberRange


class NotEqualTo(object):
    """
    Compares the values of two fields.

    Parameters
    ----------
    fieldname:
        The name of the other field to compare to
    message:
        Error message to raise in case of a validation error.  Can be
        interpolated with `%(other_label)s` and `$(other_name)s` to provide a
        more helpful error.
    """

    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data == other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('Field must be different from %(other_name)s.')
            raise ValidationError(message % d)


class ValidateFrequency(object):
    """
    Custom validator for frequency field.  Requires input of wavelet type field.

    Parameters
    ----------
    fieldname : str
        The name of the wavelet type form field
    message : str
        default message to pass
    """

    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        msg = self.message
        try:
            wavelet_type = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if int(wavelet_type.data) == 1:
            # Ormsby wavelet type has value of 1, so check this case first.
            try:
                freqs = [int(x) for x in field.data.split(',')]  # Ormsby filter should be entered as F1, F2, F3, F4
                # check that four frequencies are entered
                if len(freqs) != 4:
                    msg = "Wrong number of frequency corner points supplied or not properly formatted."
                    raise ValidationError
                # check that all frequencies are positive
                for x in freqs:
                    if x < 0:
                        msg = "Negative frequency entered.  All frequencies need to be positive."
                        raise ValidationError
                # check that frequencies increase in size
                if not freqs[0] < freqs[1] < freqs[2] < freqs[3]:
                    msg = "Frequencies should increase in value: F1 < F2 < F3 < F4."
                    raise ValidationError
            except ValidationError:
                raise ValidationError(msg)
            except AttributeError:
                if msg is None:
                    msg = "Incorrect type passed"
                raise AttributeError(msg)
        else:
            # Ricker wavelet type has value of 0, so check that case second.
            try:
                freqs = [int(x) for x in field.data.split(',')]  # Ricker filter should only have one frequency Fc
                # check that only one frequency is entered
                if len(freqs) != 1:
                    msg = "Too many frequencies entered. Ricker wavelet only takes one frequency."
                    raise ValidationError
                # check that all frequencies are positive
                if freqs[0] < 0:
                    msg = "Negative frequency entered. Only positive values accepted."
                    raise ValidationError
            except ValidationError:
                raise ValidationError(msg)
            except AttributeError:
                if msg is None:
                    msg = "Incorrect type passed"
                raise AttributeError(msg)


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
    layer_1_vp = IntegerField('vp_1', validators=[DataRequired(), NumberRange(min=0, max=20000)])
    layer_1_dens = DecimalField('rho_1', validators=[DataRequired(), NumberRange(min=1.0, max=5.0)], places=3)
    layer_1_impedance = IntegerField('imp_1')
    # layer_3 properties will be the same as layer_1
    layer_2_vp = IntegerField('vp_2', validators=[DataRequired(), NumberRange(min=0, max=20000)])
    layer_2_dens = DecimalField('rho_2', validators=[DataRequired(), NumberRange(min=1.0, max=5.0)], places=3)
    layer_2_impedance = IntegerField('imp_2', validators=[NotEqualTo(
        'layer_1_impedance',
        message='Impedances are the '
                'same and will not '
                'produce a reflection.'
    )])
    vp_units = RadioField(label='Vp Units', choices=[('0', 'm/s'), ('1', 'ft/s')], coerce=int)
    wv_type = SelectField(label='Wavelet', choices=[('0', 'Ricker'), ('1', 'Ormsby')], coerce=int)
    frequency = StringField('Frequency (Hz)', validators=[DataRequired(), ValidateFrequency('wv_type')])
    wv_length = DecimalField('Duration (s)', places=3, validators=[DataRequired(), NumberRange(min=0.01, max=1.0)])
    wv_dt = DecimalField('dt (s)',
                         places=3,
                         validators=[
                             DataRequired(),
                             NumberRange(min=0.0009, max=0.0041, message="dt must be between 0.001 and 0.004")
                         ]
                         )
    submit = SubmitField('Calculate')
