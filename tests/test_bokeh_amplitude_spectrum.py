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
from app.main import bokeh_amplitude_spectrum as bas
from bokeh.plotting import figure
import numpy as np


class BokehAmplitudeSpectrumTestCase(unittest.TestCase):

    def setUp(self):
        self.duration = 0.200
        self.dt = 0.001

    def test_plot_amplitude_spectrum(self):
        self.assertIsInstance(self.duration, float)
        self.assertIsInstance(self.dt, float)
        wb_wavelet = wb.wavelet(self.duration, self.dt, w_type=0, f=[25])
        self.assertIsInstance(wb_wavelet, np.ndarray)
        self.assertIsInstance(bas.plot_amplitude_spectrum(wb_wavelet, self.dt), tuple)
        spectrum, phase = bas.plot_amplitude_spectrum(wb_wavelet, self.dt)
        self.assertIsInstance(type(spectrum), type(figure.__class__))
        self.assertIsInstance(type(phase), type(figure.__class__))
        
    def test_plot_amplitude_spectrum_divide_by_zero_warning(self):
        self.assertIsInstance(self.duration, float)
        self.assertIsInstance(self.dt, float)
        wb_wavelet = wb.wavelet(self.duration, self.dt, w_type=0, f=[30])
        self.assertIsInstance(wb_wavelet, np.ndarray)
        self.assertIsInstance(bas.plot_amplitude_spectrum(wb_wavelet, self.dt), tuple)
        spectrum, phase = bas.plot_amplitude_spectrum(wb_wavelet, self.dt)
        self.assertIsInstance(type(spectrum), type(figure.__class__))
        self.assertIsInstance(type(phase), type(figure.__class__))
