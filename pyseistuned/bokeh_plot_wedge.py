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
from bokeh.palettes import Viridis10, RdBu11


def plot_earth_model(imp, dt):
    """

    Parameters
    ----------
    imp : ndarray
        Impedance representation of the wedge layers
    dt : float
        wavelet sample increment in seconds

    Returns
    -------

    """
    imp = np.flipud(imp)
    t = np.linspace(0, dt*imp.shape[0], imp.shape[0])  # time axis in TWT (s)
    wt = np.linspace(0, dt*imp.shape[1], imp.shape[1])  # wedge thickness in TWT (s)
    TOOLTIPS = [
        ("Impedance", "@image{int}"),
        ("Wedge Thickness, TWT (s)", "$x{1.111}")
    ]
    tools = "crosshair, pan, reset, save, wheel_zoom"
    plot = figure(
        plot_height=300, plot_width=400,
        tooltips=TOOLTIPS, title="Earth Model",
        tools=tools,
        x_range=[0, np.max(wt)], x_axis_label="TWT Wedge Thickness (sec)",
        y_range=[np.max(t), 0], y_axis_label="TWT (sec)"
    )
    plot.image(image=[imp], x=0, y=np.max(t), dw=np.max(wt), dh=np.max(t), palette=Viridis10[::-1],
               level="image")
    plot.grid.grid_line_width = 0
    plot.toolbar.logo = None

    return plot


def plot_synth(synth, dt):
    """

    Parameters
    ----------
    synth : ndarray
        synthetic trace
    dt : float
        wavelet sample increment

    Returns
    -------

    """
    synth = np.flipud(synth)
    t = np.linspace(0, dt*synth.shape[0], synth.shape[0])  # time axis in TWT (s)
    wt = np.linspace(0, dt*synth.shape[1], synth.shape[1])  # wedge thickness in TWT (s)
    TOOLTIPS = [
        ("Amplitude", "@image"),
        ("Wedge Thickness, TWT (s)", "$x{1.111}")
    ]
    tools = "crosshair, pan, reset, save, wheel_zoom, box_zoom"
    plot = figure(
        plot_height=300, plot_width=400,
        tooltips=TOOLTIPS, tools=tools, title="Synthetic Wedge Model",
        x_range=[0, np.max(wt)], x_axis_label="TWT Wedge Thickness (sec)",
        y_range=[np.max(t), 0], y_axis_label="TWT (sec)"
    )
    # plotting wiggle trace with a little help from https://github.com/fatiando/fatiando
    # using slice notation to get every second trace
    dx = ((np.max(wt) - np.min(wt))/synth.shape[1])*2
    for i, trace in enumerate(synth.transpose()[::2, :]):
        tr = trace*7*dx
        x = 0 + i*dx
        plot.line(x=x + tr, y=np.flipud(t), line_color="black", line_alpha=0.5)
    # plot synthetic as image
    plot.image(image=[synth], x=0, y=np.max(t), dw=np.max(wt), dh=np.max(t),
               palette=RdBu11[::-1], level="image")
    plot.grid.grid_line_width = 0
    plot.toolbar.logo = None

    return plot
