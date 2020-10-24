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

from flask import render_template, redirect, url_for, request, session, current_app
from . import main
from .. email import send_email
from . forms import ContactForm, TuningWedgeForm
from . import wedgebuilder as wb
from . import bokeh_wavelet as bwv
from . import bokeh_amplitude_spectrum as bas
from . import bokeh_plot_wedge as bwg
from . import bokeh_tuning_curve as btc
from bokeh.embed import components
from bokeh.models import Panel, Tabs


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    form = TuningWedgeForm(
        layer_1_vp=session.get('vp_1', 0)/1000, layer_1_dens=session.get('rho_1', 0)/1000,
        layer_2_vp=session.get('vp_2', 0)/1000, layer_2_dens=session.get('rho_2', 0)/1000,
        layer_3_vp=session.get('vp_3', 0)/1000, layer_3_dens=session.get('rho_3', 0)/1000,
        vp_units=session.get('vp_units', 0), wv_type=session.get('wv_type', 0.100),
        frequency=session.get('freq', 0), wv_length=session.get('wv_len', 100)/1000,
        wv_dt=session.get('wv_dt', 1)/1000
    )
    if form.validate_on_submit():
        # capture inputs to session dictionary ... decimals cannot be JSONified, so multiply by 1000 and cast to int
        session['vp_1'] = int(form.layer_1_vp.data * 1000)
        session['rho_1'] = int(form.layer_1_dens.data * 1000)
        session['vp_2'] = int(form.layer_2_vp.data * 1000)
        session['rho_2'] = int(form.layer_2_dens.data * 1000)
        session['vp_3'] = int(form.layer_1_vp.data * 1000)
        session['rho_3'] = int(form.layer_1_dens.data * 1000)
        session['vp_units'] = form.vp_units.data
        session['wv_type'] = form.wv_type.data
        session['freq'] = form.frequency.data
        session['wv_len'] = int(form.wv_length.data * 1000)
        session['wv_dt'] = int(form.wv_dt.data * 1000)
        return redirect(url_for('.results'))
    return render_template('index.html', form=form)


@main.route('/results', methods=['GET', 'POST'])
def results():
    # assign values from TuningWedgeForm, dividing decimal values by 1000 to recover input value
    layer_1_vp = session.get('vp_1') / 1000
    layer_1_dens = session.get('rho_1') / 1000
    layer_2_vp = session.get('vp_2') / 1000
    layer_2_dens = session.get('rho_2') / 1000
    layer_3_vp = session.get('vp_3') / 1000
    layer_3_dens = session.get('rho_3') / 1000
    vp_units = session.get('vp_units')
    wv_type = session.get('wv_type')
    # depending on whether a Ricker or Ormsby wavelet is requested, we may have more than one value
    # split the input string by comma and then typecast to int
    freq_str = session.get('freq')
    freq = [int(x) for x in freq_str.split(',')]
    wv_len = float(session.get('wv_len')) / 1000
    wv_dt = float(session.get('wv_dt')) / 1000

    # create the tuning wedge model, theoretical tuning parameters, & tuning curve
    rock_props = [layer_1_vp, layer_1_dens, layer_2_vp, layer_2_dens, layer_3_vp, layer_3_dens]
    acoustic_impedance = wb.impedance_model(rock_props)
    rc, imp = wb.earth_model(rock_props)
    wavelet = wb.wavelet(wv_len, wv_dt, wv_type, freq)
    f_central = wb.get_central_frequency(wv_type, freq)
    tuning_onset = wb.get_theoretical_onset_tuning_thickness(f_central)
    tuning = wb.get_theoretical_tuning_thickness(f_central)
    resolution_limit = wb.get_theoretical_resolution_limit(f_central)
    synth = wb.tuning_wedge(rc, wavelet)
    z = wb.get_wedge_thickness(synth, wv_dt)
    z_apparent = wb.get_apparent_wedge_thickness(synth, wv_dt, acoustic_impedance)
    tuning_meas = wb.get_measured_tuning_thickness(synth, wv_dt, acoustic_impedance)
    onset_meas = wb.get_measured_onset_tuning_thickness(z, z_apparent, f_central)
    amp = wb.get_tuning_curve_amplitude(acoustic_impedance, synth)

    # build wavelet plot and create bokeh script and div
    wavelet_plot = bwv.plot_wavelet(wavelet, wv_len)
    wv_script, wv_div = components(wavelet_plot)

    # build amplitude spectrum & phase plots and create script & div
    amplitude_spectrum, phase_plot = bas.plot_amplitude_spectrum(wavelet, wv_dt)
    ampspec_script, ampspec_div = components(amplitude_spectrum)
    phase_script, phase_div = components(phase_plot)

    # Get the synthetic wedge and earth model plots
    earth_mod = bwg.plot_earth_model(imp, wv_dt)
    synth_mod = bwg.plot_synth(synth, wv_dt, tuning_meas, onset_meas)

    # put the synthetic wedge and earth model plots together in a tabbed panel
    tab1 = Panel(child=synth_mod, title="Synthetic Wedge")
    tab2 = Panel(child=earth_mod, title="Earth Model")
    wedge_script, wedge_div = components(Tabs(tabs=[tab1, tab2]))

    # build the tuning curve plot and get script and div
    tuning_curve = btc.plot_tuning_curve(z, amp, z_apparent, tuning_meas, onset_meas)
    tc_script, tc_div = components(tuning_curve)
    return render_template('results.html',
                           vp_1=layer_1_vp, rho_1=layer_1_dens,
                           vp_2=layer_2_vp, rho_2=layer_2_dens,
                           vp_units=vp_units, wv_type=wv_type,
                           freq=freq, wv_len=wv_len, wv_dt=wv_dt,
                           wv_div=wv_div, wv_script=wv_script,
                           ampspec_div=ampspec_div, ampspec_script=ampspec_script,
                           phase_script=phase_script, phase_div=phase_div,
                           wedge_script=wedge_script, wedge_div=wedge_div,
                           tc_script=tc_script, tc_div=tc_div,
                           tuning_twt=tuning, tuning_twt_onset=tuning_onset,
                           tuning_twt_meas=tuning_meas, tuning_twt_onset_meas=onset_meas,
                           res_lim=resolution_limit
                           )


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        body = request.form.get('body')
        send_email(subject, email, name, [current_app.config['ADMINS'][0]], body)
        return redirect(url_for('.success'))
    return render_template('contact.html', form=form)


@main.route('/success')
def success():
    return render_template('success.html')
