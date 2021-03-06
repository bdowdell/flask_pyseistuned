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


def plot_wavelet(w, duration):
    """

    Parameters
    ----------
    w : ndarray
        numpy ndarray containing wavelet amplitude values
    duration : float
        length of wavelet

    Returns
    -------

    """
    # set up data
    start = int(duration * 1000 / 2 * - 1 - 1)
    stop = int(duration * 1000 / 2)
    num = len(w)
    x = np.linspace(start, stop, num)
    source = ColumnDataSource(data=dict(x=x, y=w))

    # set up plot
    TOOLTIPS = [
        ("Time", "$x ms"),
        ("Amp", "$y")
    ]
    plot = figure(plot_height=250, plot_width=250, tooltips=TOOLTIPS, title="Wavelet",
                  tools="crosshair,pan,reset,save,wheel_zoom",
                  x_range=[np.min(x), np.max(x)], y_range=[np.min(w) - 0.1, np.max(w) + 0.1])
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
    plot.xaxis.axis_label = "Time (ms)"

    return plot
