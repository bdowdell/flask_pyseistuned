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
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearAxis, Range1d, Span


def plot_tuning_curve(z, amp, z_apparent, z_tuning, z_onset):
    """

    Parameters
    ----------
    z : ndarray
        wedge thickness in milliseconds
    amp : ndarray
        amplitude along top of wedge
    z_apparent : ndarray
        apparent wedge thickness in milliseconds
    z_tuning : float
        measured tuning thickness
    z_onset : float
        measured onset of tuning

    Returns
    -------

    """
    min_amp = np.min(np.abs(amp))
    max_amp = np.max(np.max(amp))
    source = ColumnDataSource(data=dict(x=z, y=amp, z=z_apparent))
    TOOLTIPS = [
        ("Amplitude", "$y{1.111}"),
        ("TWT thickness", "$x{1.1} ms")
    ]
    tools = "crosshair, pan, reset, save, wheel_zoom, box_zoom"
    plot = figure(
        plot_height=300, plot_width=400,
        tooltips=TOOLTIPS, title="Tuning Curve", tools=tools,
        x_axis_label="TWT thickness (ms)", y_axis_label="Abs(Amplitude)",
        y_range=(min_amp, max_amp + 0.01)
    )
    plot.line('x', 'y', source=source, line_width=3)
    # add wedge true & measured thickness to plot
    plot.extra_y_ranges = {"thickness": Range1d(start=0, end=np.max(z))}
    plot.add_layout(LinearAxis(y_range_name="thickness", axis_label="TWT thickness (ms)"), "left")
    plot.line('x', 'x', source=source, line_width=2, line_alpha=0.6, line_color="green", y_range_name="thickness")
    plot.line('x', 'z', source=source, line_width=2, line_alpha=0.6, line_color="red", y_range_name="thickness")
    z_tuning_vline = Span(location=z_tuning, dimension="height", line_color="black", line_width=2)
    plot.add_layout(z_tuning_vline)
    z_onset_vline = Span(location=z_onset, dimension="height", line_color="black", line_dash="dashed", line_width=2)
    plot.add_layout(z_onset_vline)
    plot.toolbar.logo = None

    return plot
