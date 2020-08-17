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

from flask import Flask, render_template, flash, redirect, url_for
from config import Config
from pyseistuned.forms import ContactForm, TuningWedgeForm


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = TuningWedgeForm(units=0, wv_length=0.100, wv_dt=0.001)
    return render_template('index.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Email sent!')
        return redirect(url_for('success'))
    return render_template('contact.html', form=form)


@app.route('/success')
def success():
    return render_template('success.html')
