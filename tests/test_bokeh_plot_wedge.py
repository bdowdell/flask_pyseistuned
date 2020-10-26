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
from app.main import bokeh_plot_wedge as bpw
import numpy as np
from bokeh.plotting import figure


class BokehPlotWedgeTestCase(unittest.TestCase):

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

    def test_plot_earth_model(self):
        self.assertIsInstance(self.imp, np.ndarray)
        self.assertEqual(self.imp.shape, (240, 101))
        self.assertIsInstance(self.dt, float)
        imp_plot = bpw.plot_earth_model(self.imp, self.dt)
        self.assertIsInstance(type(imp_plot), type(figure.__class__))

    def test_plot_synth(self):
        self.assertIsInstance(self.synth, np.ndarray)
        self.assertEqual(self.synth.shape, (240, 101))
        self.assertIsInstance(self.dt, float)
        self.assertIsInstance(self.tuning_meas, float)
        self.assertIsInstance(self.onset_meas, int)
        synth_plot = bpw.plot_synth(self.synth, self.dt, self.tuning_meas, self.onset_meas)
        self.assertIsInstance(type(synth_plot), type(figure.__class__))
