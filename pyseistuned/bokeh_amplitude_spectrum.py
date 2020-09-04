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

import numpy as np

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


def plot_amplitude_spectrum(w, dt):
    """

    Parameters
    ----------
    w : ndarray
        numpy ndarray containing wavelet amplitude values
    dt : float
        wavelet sample increment

    Returns
    -------

    """
    # get the amplitude spectrum of the wavelet using discrete Fourier transform
    # note: power_spectrum = amplitude_spectrum**2 and dB scale if 20*np.log10(amplitude_spectrum)
    amplitude_spectrum = abs(np.fft.rfft(w))
    amp_dB = 20 * np.log10(amplitude_spectrum/np.max(amplitude_spectrum))
    phase = np.angle(amplitude_spectrum, deg=True)
    nyquist = 1 / (2 * dt)

    # define x-axis
    x = np.fft.rfftfreq(w.size, d=dt)

    # set up column data source
    spectrum_source = ColumnDataSource(data=dict(x=x, y=amp_dB))
    phase_source = ColumnDataSource(data=dict(x=x, y=phase))

    # set up spectrum plot
    spec_TOOLTIPS = [
        ("Frequency", "$x"),
        ("Amplitude", "$y")
    ]

    spectrum_plot = figure(plot_height=250, plot_width=250, tooltips=spec_TOOLTIPS, title="Amplitude Spectrum",
                           tools="crosshair, pan, box_zoom, reset, save",
                           x_range=[0, np.max(x)])
    spectrum_plot.line('x', 'y', source=spectrum_source, line_width=3, line_alpha=0.6)
    spectrum_plot.xaxis.axis_label = "Frequency (Hz)"
    spectrum_plot.yaxis.axis_label = "Amplitude (dB)"

    # set up phase plot
    phase_TOOLTIPS = [
        ("Frequency", "$x"),
        ("Phase", "$y")
    ]

    phase_plot = figure(plot_height=250, plot_width=250, tooltips=phase_TOOLTIPS, title="Phase",
                        tools="crosshair, pan, reset, save, wheel_zoom",
                        x_range=[0, nyquist], y_range=[-180, 180])
    phase_plot.line('x', 'y', source=phase_source, line_width=3, line_alpha=0.6)
    phase_plot.xaxis.axis_label = "Frequency (Hz)"
    phase_plot.yaxis.axis_label = "Phase (degrees)"

    return spectrum_plot, phase_plot
