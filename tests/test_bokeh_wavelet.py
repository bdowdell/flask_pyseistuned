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
from app.main import bokeh_wavelet as bwv
from bokeh.plotting import figure
import numpy as np


class BokehWaveletTestCase(unittest.TestCase):

    def setUp(self):
        self.duration = 0.200
        self.dt = 0.001

    def test_plot_wavelet(self):
        self.assertIsInstance(self.duration, float)
        self.assertIsInstance(self.dt, float)
        wb_wavelet = wb.wavelet(self.duration, self.dt, w_type=0, f=[25])
        self.assertIsInstance(wb_wavelet, np.ndarray)
        wavelet_plot = bwv.plot_wavelet(wb_wavelet, self.duration)
        self.assertIsInstance(type(wavelet_plot), type(figure.__class__))  # <class 'bokeh.plotting.figure.Figure'>
