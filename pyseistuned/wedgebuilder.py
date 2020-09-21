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


def earth_model(rock_props):
    """Builds a earth model using input Vp-Density pairs and calculates reflection coefficients and layer impedance.

    Parameters
    ----------
    rock_props : list
        A list of len 6 containing Vp-Density pairs for the three layers

    Returns
    -------
    rc : ndarray
        Numpy ndarray containing reflection coefficients
    imp : ndarray
        Numpy ndarray containing layer impedance

    """
    # define the earth model
    width, height = 101, 240
    model = 1 + np.tri(height, width, -height // 3, dtype=int)
    model[: height // 3, :] = 0

    # reshape the input rock properties list for populating earth model
    rocks = np.array(rock_props).reshape(3, 2)

    # use fancy indexing to create an earth model where each layer of the model
    # has Vp & Density at each location
    earth = rocks[model]

    # calculate the acoustic impedance of each layer
    imp = np.apply_along_axis(np.product, -1, earth)

    # calculate the reflection coefficients for the interfaces between each layer
    rc = np.zeros(imp.shape, dtype=float)
    rc[1:, :] = (imp[1:, :] - imp[:-1, :]) / (imp[1:, :] + imp[:-1, :])

    return rc, imp


def rc_mask(rc):
    """Creates a mask for where RC is 0
    
    Parameters
    ----------
    rc : ndarray
        Numpy array of reflection coefficients

    Returns
    -------
    ndarray
        A masked ndarray for zero values

    """
    return np.ma.masked_equal(rc, 0)


def wavelet(duration=0.100, dt=0.001, w_type=0, f=None):
    """This function defines a wavelet to convolve with the earth model reflection coefficients

    Parameters
    ----------
    duration : float
        length in seconds of wavelet
    dt : float
        sample increment of wavelet
    w_type : int
        Wavelet type. 0 is Ricker, 1 is Ormsby
    f : list
        dominant frequency of wavelet

    Returns
    -------
    ndarray
        wavelet amplitude

    """
    if f is None:
        f = [25]
    t = np.linspace(-duration / 2, (duration - dt) / 2, int(duration / dt))
    if w_type:
        # Ormsby wavelet
        f1, f2, f3, f4 = [x for x in f]
        a = ((np.pi * f4)**2)/((np.pi * f4) - (np.pi * f3))
        b = ((np.pi * f3)**2)/((np.pi * f4) - (np.pi * f3))
        c = ((np.pi * f2)**2)/((np.pi * f2) - (np.pi * f1))
        d = ((np.pi * f1)**2)/((np.pi * f2) - (np.pi * f1))
        w = (((a * (np.sinc(f4 * t))**2) - (b * (np.sinc(f3 * t))**2)) -
             ((c * (np.sinc(f2 * t))**2) - (d * (np.sinc(f1 * t))**2)))
    else:
        # Ricker wavelet
        f = f[0]
        w = (1.0 - 2.0 * (np.pi ** 2) * (f ** 2) * (t ** 2)) * np.exp(
            -(np.pi ** 2) * (f ** 2) * (t ** 2)
        )
    return np.squeeze(w) / np.amax(w)


def tuning_wedge(rc, w):
    """Calculates synthetic tuning wedge based on reflection coefficients and wavelet

    Parameters
    ----------
    rc : ndarray
        ndarray of reflection coefficients
    w : ndarray
        wavelet

    Returns
    -------
    ndarray
        ndarray of synthetic tuning wedge

    """
    synth = np.apply_along_axis(lambda t: np.convolve(t, w, mode="same"), axis=0, arr=rc)
    return synth


def tuning_curve(synth, rock_props, dt, w_type, f=None):
    """Calculates the tuning curve

    Parameters
    ----------
    synth : ndarray
        array of synthetic seismic values
    rock_props : list
        list of rock properties (Vp, Density)
    dt : float
        wavelet sample increment
    w_type : int
        Wavelet type. 0 for Ricker, 1 for Ormsby
    f : list
        wavelet frequency(ies)

    Returns
    -------
    z : ndarray
        wedge thickness
    z_tuning : float
        tuning thickness in TWT
    amp : ndarray
        extracted amplitude along the top of the wedge model
    z_apparent : ndarray
        apparent wedge thickness
    z_onset : int
        wedge thickness at onset of tuning
    tuning_onset : float
        tuning onset thickness in milliseconds
    tuning : float
        tuning thickness in milliseconds
    resolution_limit : float
        limit of resolution in milliseconds

    """

    # Get central frequency depending on wavelet type, first set default value if not passed in
    if f is None:
        f = [25]
    if w_type:
        # take average of low pass and high pass in Ormsby filter
        f_central = (f[1] + f[2]) / 2
        tuning_onset = 1 / f_central * 1000
        tuning = tuning_onset / 2
        resolution_limit = 1 / f_central / 4 * 1000
    else:
        # Ricker central frequency
        f_central = f[0]
        f_apparent = f_central * np.pi / np.sqrt(6)
        tuning_onset = 1 / f_apparent * 1000
        tuning = tuning_onset / 2
        resolution_limit = 1 / f_apparent / 4 * 1000

    rocks = np.array(rock_props).reshape(3, 2)
    AI = np.apply_along_axis(np.product, -1, rocks)

    # create an ndarray containing index value of top of wedge
    if AI[1] < AI[0]:
        top_idx = np.nanargmin(synth[:, -1])  # use the last column in model to get top at min amplitude
    else:
        top_idx = np.nanargmax(synth[:, -1])  # use the last column in model to get top at max amplitude

    top = np.ones(synth.shape[1], dtype=int) * top_idx

    # calculate the wedge thickness
    z = np.zeros(synth.shape[1])
    z[1:] += dt
    z = np.cumsum(z) * 1000
    z = z.astype(np.int64)  # force wedge thicknesses to be integers

    # determine the thickness at which synth has max amplitude
    # This is the measured tuning thickness in TWT
    z_tuning_idx = np.nanargmax(abs(synth[np.nanmax(top), :]))
    z_tuning_arr = np.zeros(z_tuning_idx + 1)
    z_tuning_arr[1:] += dt
    z_tuning_arr = np.cumsum(z_tuning_arr) * 1000
    z_tuning = z_tuning_arr[-1]

    # determine the apparent thickness at which synth has max amplitude
    # this represents what is seismically resolvable, in TWT
    if AI[1] < AI[0]:
        top_apparent = np.apply_along_axis(np.nanargmin, 0, synth)
        base_apparent = np.apply_along_axis(np.nanargmax, 0, synth)
    else:
        top_apparent = np.apply_along_axis(np.nanargmax, 0, synth)
        base_apparent = np.apply_along_axis(np.nanargmin, 0, synth)

    z_apparent = base_apparent - top_apparent
    z_apparent[0] = z_apparent[1]  # project the minimum apparent thickness to the first index
    z_apparent = z_apparent * dt * 1000
    z_apparent = z_apparent.astype(np.int64)

    # extract the amplitude along the top of the wedge model
    amp = abs(synth[top, :])

    # sometimes if frequency is very low and the sample increment is small, the wedge will not be wide enough to get
    # the tuning onset and will result in an IndexError.  When that happens, return theoretical onset instead.
    try:
        # calculate the tuning onset thickness based on divergence between true and apparent wedge thickness
        z_onset_idx = np.argwhere(z - z_apparent > 0)[-1][0] + 1  # the last value is where thinning causes tuning onset
        z_onset = z_apparent[z_onset_idx]
    except IndexError:
        z_onset = int((1 / (np.pi / np.sqrt(6) * f_central)) * 1000)

    return z, z_tuning, amp, z_apparent, z_onset, tuning_onset, tuning, resolution_limit
