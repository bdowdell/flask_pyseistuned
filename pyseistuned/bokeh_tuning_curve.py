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
from bokeh.models import ColumnDataSource


def plot_tuning_curve(z, amp):
    """

    Parameters
    ----------
    z : ndarray
        wedge thickness in milliseconds
    amp : ndarray
        amplitude along top of wedge

    Returns
    -------

    """
    source = ColumnDataSource(data=dict(x=z, y=amp))
    TOOLTIPS = [
        ("Amplitude", "$y{1.111}"),
        ("TWT thickness (ms)", "$x{1.1}")
    ]
    tools = "crosshair, pan, reset, save, wheel_zoom, box_zoom"
    plot = figure(
        plot_height=300, plot_width=400,
        tooltips=TOOLTIPS, title="Tuning Curve", tools=tools,
        x_axis_label="TWT thickness (ms)", y_axis_label="Amplitude"
    )
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
    plot.toolbar.logo = None

    return plot
