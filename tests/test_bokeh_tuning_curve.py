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

import unittest
from app.main import wedgebuilder as wb
from app.main import bokeh_tuning_curve as btc
import numpy as np
from bokeh.plotting import figure


class BokehTuningCurveTestCase(unittest.TestCase):
    
    def setUp(self):
        self.rock_props = [3000, 2.5, 2700, 2.3, 3000, 2.5]
        self.acoustic_impedance = wb.impedance_model(self.rock_props)
        self.duration = 0.200
        self.dt = 0.001
        self.f = [25]
        self.f_central = wb.get_central_frequency(w_type=0, f=self.f)
        self.rc, self.imp = wb.earth_model(self.rock_props)
        self.wavelet = wb.wavelet(self.duration, self.dt, w_type=0, f=self.f)
        self.synth = wb.tuning_wedge(self.rc, self.wavelet)
        self.true_wedge_thickness = wb.get_wedge_thickness(self.synth, self.dt)
        self.apparent_wedge_thickness = wb.get_apparent_wedge_thickness(self.synth, self.dt, self.acoustic_impedance)
        self.tuning_meas = wb.get_measured_tuning_thickness(self.synth, self.dt, self.acoustic_impedance)
        self.onset_meas = wb.get_measured_onset_tuning_thickness(
            self.true_wedge_thickness, self.apparent_wedge_thickness, self.f_central
        )
        self.amplitude = wb.get_tuning_curve_amplitude(self.acoustic_impedance, self.synth)
        
    def test_plot_tuning_curve(self):
        self.assertIsInstance(self.true_wedge_thickness, np.ndarray)
        self.assertGreaterEqual(np.min(self.true_wedge_thickness), 0)
        self.assertIsInstance(self.amplitude, np.ndarray)
        self.assertGreaterEqual(np.min(self.amplitude), 0)
        self.assertIsInstance(self.apparent_wedge_thickness, np.ndarray)
        self.assertGreaterEqual(np.min(self.apparent_wedge_thickness), 0)
        self.assertEqual(self.true_wedge_thickness.shape, self.apparent_wedge_thickness.shape)
        self.assertIsInstance(self.tuning_meas, float)
        self.assertGreater(self.tuning_meas, 0)
        self.assertIsInstance(self.onset_meas, int)
        self.assertGreater(self.onset_meas, 0)
        tuning_curve = btc.plot_tuning_curve(
            self.true_wedge_thickness,
            self.amplitude,
            self.apparent_wedge_thickness,
            self.tuning_meas,
            self.onset_meas
        )
        self.assertIsInstance(type(tuning_curve), type(figure.__class__))
