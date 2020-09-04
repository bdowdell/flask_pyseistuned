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

from flask import Flask, render_template, redirect, url_for, request
from config import Config
from pyseistuned.forms import ContactForm, TuningWedgeForm
from flask_mail import Mail, Message
import pyseistuned.wedgebuilder as wb
import pyseistuned.bokeh_wavelet as bokeh_wavelet
import pyseistuned.bokeh_amplitude_spectrum as bas
from bokeh.embed import components


app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = TuningWedgeForm(vp_units=0, wv_length=0.100, wv_dt=0.001)
    if form.validate_on_submit():
        return redirect(url_for('results', form=request.form))
    return render_template('index.html', form=form)


@app.route('/results', methods=['GET', 'POST'])
def results():
    # assign values from TuningWedgeForm
    layer_1_vp = float(request.form.get('layer_1_vp'))
    layer_1_dens = float(request.form.get('layer_1_dens'))
    layer_2_vp = float(request.form.get('layer_2_vp'))
    layer_2_dens = float(request.form.get('layer_2_dens'))
    layer_3_vp = float(request.form.get('layer_3_vp'))
    layer_3_dens = float(request.form.get('layer_3_dens'))
    vp_units = int(request.form.get('vp_units'))
    wv_type = int(request.form.get('wv_type'))
    freq_str = request.form.get('frequency')
    # depending on whether a Ricker or Ormsby wavelet is requested, we may have more than one value
    # split the input string by comma and then typecast to int
    freq = freq_str.split(',')
    freq = [int(x) for x in freq]
    wv_len = float(request.form.get('wv_length'))
    wv_dt = float(request.form.get('wv_dt'))

    # create the tuning wedge model and tuning curve
    rock_props = [layer_1_vp, layer_1_dens, layer_2_vp, layer_2_dens, layer_3_vp, layer_3_dens]
    rc, imp = wb.earth_model(rock_props)
    wavelet = wb.wavelet(wv_len, wv_dt, wv_type, freq)
    synth = wb.tuning_wedge(rc, wavelet)
    z, z_tuning, amp, z_apparent, z_onset = wb.tuning_curve(rc, synth, rock_props)

    wavelet_plot = bokeh_wavelet.plot_wavelet(wavelet, wv_len)
    wv_script, wv_div = components(wavelet_plot)

    amplitude_spectrum, phase_plot = bas.plot_amplitude_spectrum(wavelet, wv_dt)
    ampspec_script, ampspec_div = components(amplitude_spectrum)
    phase_script, phase_div = components(phase_plot)

    return render_template('results.html',
                           vp_1=layer_1_vp, rho_1=layer_1_dens,
                           vp_2=layer_2_vp, rho_2=layer_2_dens,
                           vp_3=layer_3_vp, rho_3=layer_3_dens,
                           vp_units=vp_units, wv_type=wv_type,
                           freq=freq, wv_len=wv_len, wv_dt=wv_dt,
                           wv_div=wv_div, wv_script=wv_script,
                           ampspec_div=ampspec_div, ampspec_script=ampspec_script,
                           phase_script=phase_script, phase_div=phase_div
                           )


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        body = request.form.get('body')
        msg = Message(subject=subject,
                      sender=email,
                      recipients=[app.config['ADMINS'][0]],
                      extra_headers={'name': name}
                      )
        msg.body = body
        mail.send(msg)
        return redirect(url_for('success'))
    return render_template('contact.html', form=form)


@app.route('/success')
def success():
    return render_template('success.html')
