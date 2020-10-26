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


def impedance_model(rock_props):
    """

    Parameters
    ----------
    rock_props : list
        A list of len 6 containing Vp-Density pairs for each of the three layers

    Returns
    -------
    ndarray

    """
    # calculate AI
    rocks = np.array(rock_props).reshape(3, 2)
    acoustic_impedance = np.apply_along_axis(np.product, -1, rocks)
    return acoustic_impedance


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
        if w_type:
            f = [5, 10, 50, 100]
        else:
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
        # Ricker wavelet defined in terms of F_central instead of F_peak so that the period
        # can be used to estimated tuning with the frequency expected by the user
        f = f[0] / (np.pi / np.sqrt(6))
        w = (1.0 - 2.0 * (np.pi ** 2) * (f ** 2) * (t ** 2)) * np.exp(
            -(np.pi ** 2) * (f ** 2) * (t ** 2)
        )
    return np.squeeze(w) / np.amax(w)


def get_central_frequency(w_type, f=None):
    """

    Parameters
    ----------
    w_type : int
        Wavelet type. 0 is Rikcer, 1 is Ormsby
    f : list
        frequency parameters of wavelet

    Returns
    -------
    int

    """
    if f is None:
        f = [25]
    if w_type:
        return int((f[0] + f[3]) / 2)
    else:
        return f[0]


def get_theoretical_onset_tuning_thickness(f_central):
    """

    Parameters
    ----------
    f_central : float
        wavelet central frequency in Hz

    Returns
    -------
    float

    """
    return 1 / f_central * 1000


def get_theoretical_tuning_thickness(f_central):
    """

    Parameters
    ----------
    f_central : float
        wavelet central frequency in Hz

    Returns
    -------
    float

    """
    return 1 / f_central / 2 * 1000


def get_theoretical_resolution_limit(f_central):
    """

    Parameters
    ----------
    f_central : float
        wavelet central frequency in Hz

    Returns
    -------
    float

    """
    return 1 / f_central / 4 * 1000


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
    return np.apply_along_axis(lambda t: np.convolve(t, w, mode="same"), axis=0, arr=rc)


def get_wedge_thickness(synth, dt):
    """Calculates wedge thickness in milliseconds

    Parameters
    ----------
    synth : ndarray
        (n, m) array containing synthetic seismogram values
    dt : float
        wavelet sample increment in seconds

    Returns
    -------
    dz : ndarray
        (m, ) array containing absolute thickness of the wedge, in milliseconds

    """
    dz = np.zeros(synth.shape[1])
    dz[1:] += dt
    dz = np.cumsum(dz) * 1000
    return dz.astype(np.int64)


def get_apparent_wedge_thickness(synth, dt, acoustic_impedance):
    """

    Parameters
    ----------
    synth : ndarray
        (n, m) array containing synthetic seismogram values
    dt : float
        wavelet sample increment in seconds
    acoustic_impedance : ndarray
        (3, ) array of layer acoustic impedances

    Returns
    -------
    apparent_dz : ndarray
        (m, ) shape array containing apparent wedge thickness in milliseconds

    """
    # determine the apparent thickness at which synth has max amplitude
    # this represents what is seismically resolvable, in TWT
    if acoustic_impedance[1] < acoustic_impedance[0]:
        top_apparent = np.apply_along_axis(np.nanargmin, 0, synth)
        base_apparent = np.apply_along_axis(np.nanargmax, 0, synth)
    else:
        top_apparent = np.apply_along_axis(np.nanargmax, 0, synth)
        base_apparent = np.apply_along_axis(np.nanargmin, 0, synth)

    apparent_dz = base_apparent - top_apparent
    apparent_dz[0] = apparent_dz[1]  # project the minimum apparent thickness to the first index
    apparent_dz = apparent_dz * dt * 1000
    return apparent_dz.astype(np.int64)


def get_measured_tuning_thickness(synth, dt, acoustic_impedance):
    """

    Parameters
    ----------
    synth : ndarray
        (n, m) array containing synthetic seismogram values
    dt : float
        wavelet sample increment in seconds
    acoustic_impedance : ndarray
        (3, ) array of layer acoustic impedances

    Returns
    -------
    float

    """
    if acoustic_impedance[1] < acoustic_impedance[0]:
        top_idx = np.nanargmin(synth[:, -1])  # use the last column in model to get top at min amplitude
    else:
        top_idx = np.nanargmax(synth[:, -1])  # use the last column in model to get top at max amplitude
    top = np.ones(synth.shape[1], dtype=int) * top_idx
    # determine the thickness at which synth has max amplitude
    # This is the measured tuning thickness in TWT
    z_tuning_idx = np.nanargmax(abs(synth[np.nanmax(top), :]))
    z_tuning_arr = np.zeros(z_tuning_idx + 1)
    z_tuning_arr[1:] += dt
    z_tuning_arr = np.cumsum(z_tuning_arr) * 1000
    return z_tuning_arr[-1]


def get_measured_onset_tuning_thickness(dz, apparent_dz, f_central):
    """

    Parameters
    ----------
    dz : ndarray
        (n, ) array containing true wedge thickness in milliseconds
    apparent_dz : ndarray
        (n, ) array containing apparent wedge thickness in milliseconds
    f_central : float
        central frequency of wavelet
    Returns
    -------
    int

    """
    # sometimes if frequency is very low and the sample increment is small, the wedge will not be wide enough to get
    # the tuning onset and will result in an IndexError.  When that happens, return theoretical onset instead.
    try:
        # calculate the tuning onset thickness based on divergence between true and apparent wedge thickness
        # the last value is where thinning causes tuning onset
        onset_idx = np.argwhere(dz - apparent_dz > 0)[-1][0] + 1
        return int(apparent_dz[onset_idx])
    except IndexError:
        return int((1 / f_central) * 1000)


def get_tuning_curve_amplitude(acoustic_impedance, synth):
    """

    Parameters
    ----------
    acoustic_impedance : ndarray
        (3, ) array of layer acoustic impedances
    synth : ndarray
        (n, m) array containing sythetic seismogram values

    Returns
    -------
    ndarray

    """
    if acoustic_impedance[1] < acoustic_impedance[0]:
        top_idx = np.nanargmin(synth[:, -1])  # use the last column in model to get top at min amplitude
    else:
        top_idx = np.nanargmax(synth[:, -1])  # use the last column in model to get top at max amplitude
    return abs(synth[top_idx, :])
