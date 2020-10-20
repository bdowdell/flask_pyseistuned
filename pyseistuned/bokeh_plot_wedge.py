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
from bokeh.models import Range1d


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
    # bokeh's image plots upside down, so need to flip the impedance ndarray
    imp = np.flipud(imp)

    # time axis in TWT (millisec)
    t = np.zeros(imp.shape[0])
    t[1:] += dt
    t = np.cumsum(t) * 1000

    # wedge thickness in TWT (millisec)
    wt = np.zeros(imp.shape[1])
    wt[1:] += dt
    wt = np.cumsum(wt) * 1000

    # set plot configuration
    TOOLTIPS = [
        ("Impedance", "@image{int}"),
        ("TWT", "$y{1.1} ms"),
        ("Wedge Thickness", "$x{1.1} ms")
    ]
    tools = "crosshair, pan, reset, save, wheel_zoom"
    plot = figure(
        plot_height=300, plot_width=400,
        tooltips=TOOLTIPS, title="Earth Model",
        tools=tools,
        x_range=Range1d(0, 100), x_axis_label="TWT Wedge Thickness (ms)",
        y_range=[np.max(t), 0], y_axis_label="TWT (ms)"
    )
    plot.image(image=[imp], x=0, y=np.max(t), dw=np.max(wt), dh=np.max(t), palette=Viridis10[::-1],
               level="image")
    plot.grid.grid_line_width = 0
    plot.toolbar.logo = None

    return plot


def plot_synth(synth, dt, z_tuning, z_onset):
    """

    Parameters
    ----------
    synth : ndarray
        synthetic trace
    dt : float
        wavelet sample increment
    z_tuning : float
        tuning thickness in TWT milliseconds
    z_onset : int
        onset of tuning in TWT milliseconds

    Returns
    -------

    """
    # bokeh's image plots upside down, so need to flip the impedance ndarray
    synth = np.flipud(synth)

    # time axis in TWT (millisec)
    t = np.zeros(synth.shape[0])
    t[1:] += dt
    t = np.cumsum(t) * 1000

    # wedge thickness in TWT (millisec)
    wt = np.zeros(synth.shape[1])
    wt[1:] += dt
    wt = np.cumsum(wt) * 1000
    tuning_idx = np.argwhere(wt == z_tuning)[0][0]  # get TWT tuning thickness index

    # set plot configuration
    TOOLTIPS = [
        ("Amplitude", "@image"),
        ("TWT", "$y{1.1} ms"),
        ("Wedge Thickness", "$x{1.1} ms")
    ]
    tools = "crosshair, pan, reset, save, wheel_zoom, box_zoom"
    plot = figure(
        plot_height=300, plot_width=400,
        tooltips=TOOLTIPS, tools=tools, title="Synthetic Wedge Model",
        x_range=Range1d(0, wt[-1]), x_axis_label="TWT Wedge Thickness (ms)",
        y_range=[np.max(t), 0], y_axis_label="TWT (ms)"
    )

    # plotting wiggle trace with a little help from https://github.com/fatiando/fatiando
    # using slice notation to get every second trace
    dx = int(round(((np.max(wt) - np.min(wt))/synth.shape[1])*2))  # x-axis increment
    synth_min = synth.min()  # min value of synthetic for normalization
    synth_max = synth.max()  # max value of synthetic for normalization
    synth_diff = synth_max - synth_min
    for i, trace in enumerate(synth.transpose()[::dx, :]):
        tr = (((trace - synth_min)/synth_diff) - 0.5)*4*dx
        x = wt[i*dx]
        plot.line(x=x + tr, y=np.flipud(t), line_color="black", line_alpha=0.5)
    # plot synthetic trace at measured tuning TWT thickness
    plot.line(
        x=(tuning_idx * dt * 1000 + (((synth.transpose()[tuning_idx, :] - synth_min)/synth_diff) - 0.5) * 4 * dx),
        y=np.flipud(t), line_color="black", line_width=3
    )

    # If wavelet frequency is low (<10 Hz) and sample increment is small (==0.001), the wedge is not thick enough
    # to establish the tuning onset thickness, so we will omit it from the plot in that case.
    try:
        # get TWT onset tuning thickness index
        onset_idx = np.argwhere(wt.astype(np.int64) == z_onset)[0][0]
        # plot synthetic trace at measured onset tuning TWT thickness
        plot.line(
            x=(onset_idx * dt * 1000 + (((synth.transpose()[onset_idx, :] - synth_min)/synth_diff) - 0.5) * 4 * dx),
            y=np.flipud(t), line_color="black", line_width=2, line_alpha=0.7, line_dash="dashed"
        )
    except IndexError:
        pass

    # plot synthetic as image
    plot.image(image=[synth], x=0, y=np.max(t), dw=wt[-1], dh=np.max(t),
               palette=RdBu11[::-1], level="image")

    plot.grid.grid_line_width = 0
    plot.toolbar.logo = None

    return plot
