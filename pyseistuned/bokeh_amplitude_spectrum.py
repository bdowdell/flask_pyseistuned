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
    amplitude_spectrum = abs(np.fft.rfft(w))
    nyquist = 1 / (2 * dt)

    # define x-axis
    x = np.linspace(start=0, stop=nyquist, num=len(amplitude_spectrum))
    
    # set up column data source
    source = ColumnDataSource(data=dict(x=x, y=amplitude_spectrum))

    # set up plot
    plot = figure(plot_height=300, plot_width=300, title="Amplitude Spectrum",
                  tools="crosshair,pan,reset,save,wheel_zoom",
                  x_range=[0, nyquist], y_range=[0, np.max(amplitude_spectrum)])
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
    plot.xaxis.axis_label = "Frequency (Hz)"
    plot.yaxis.axis_label = "Amplitude"

    return plot
