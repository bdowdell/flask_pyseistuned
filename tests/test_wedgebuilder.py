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
import numpy as np


class WedgeBuilderTestCase(unittest.TestCase):

    def setUp(self):
        self.rock_props = [3000, 2.5, 2700, 2.3, 3000, 2.5]
        self.layer_1_impedance = self.rock_props[0] * self.rock_props[1]
        self.layer_2_impedance = self.rock_props[2] * self.rock_props[3]
        self.layer_3_impedance = self.rock_props[4] * self.rock_props[5]
        self.acoustic_impedance = np.array([
            self.layer_1_impedance,
            self.layer_2_impedance,
            self.layer_3_impedance
        ])
        self.duration = 0.200
        self.dt = 0.001

    def tearDown(self):
        pass

    def test_00_impedance_model(self):
        wb_acoustic_impedance = wb.impedance_model(self.rock_props)
        self.assertIsInstance(wb_acoustic_impedance, np.ndarray)
        self.assertEqual(len(wb_acoustic_impedance), 3)
        self.assertEqual(self.layer_1_impedance, wb_acoustic_impedance[0])
        self.assertEqual(self.layer_2_impedance, wb_acoustic_impedance[1])
        self.assertEqual(self.layer_3_impedance, wb_acoustic_impedance[2])

    def test_01_earth_model(self):
        wb_rc, wb_imp = wb.earth_model(self.rock_props)
        self.assertIsInstance(wb_rc, np.ndarray)
        self.assertEqual(wb_rc.shape, (240, 101))
        self.assertIsInstance(wb_imp, np.ndarray)
        self.assertEqual(wb_imp.shape, (240, 101))

    def test_02_wavelet_ricker(self):
        wb_wavelet = wb.wavelet(self.duration, self.dt, w_type=0, f=[30])
        self.assertIsInstance(wb_wavelet, np.ndarray)
        self.assertEqual(len(wb_wavelet), int(self.duration / self.dt))
        
    def test_03_wavelet_ormsby(self):
        wb_wavelet = wb.wavelet(self.duration, self.dt, w_type=1, f=[5, 10, 40, 50])
        self.assertIsInstance(wb_wavelet, np.ndarray)
        self.assertEqual(len(wb_wavelet), int(self.duration / self.dt))

    def test_04_get_central_frequency_ricker(self):
        wb_central_frequency = wb.get_central_frequency(w_type=0, f=[30])
        self.assertEqual(wb_central_frequency, 30)

    def test_05_get_central_frequency_ormsby(self):
        wb_central_frequency = wb.get_central_frequency(w_type=1, f=[5, 10, 40, 50])
        self.assertEqual(wb_central_frequency, int((5 + 50) / 2))

    def test_06_get_theoretical_onset_tuning_thickness(self):
        f_central = 30
        onset_thickness = 1 / f_central * 1000
        self.assertEqual(wb.get_theoretical_onset_tuning_thickness(f_central), onset_thickness)

    def test_07_get_theoretical_tuning_thickness(self):
        f_central = 30
        tuning_thickness = 1 / f_central / 2 * 1000
        self.assertEqual(wb.get_theoretical_tuning_thickness(f_central), tuning_thickness)

    def test_08_get_theoretical_resolution_limit(self):
        f_central = 30
        resolution_limit = 1 / f_central / 4 * 1000
        self.assertEqual(wb.get_theoretical_resolution_limit(f_central), resolution_limit)

    def test_09_tuning_wedge_ricker_wavelet(self):
        wb_rc, wb_imp = wb.earth_model(self.rock_props)
        # first with a wavelet with duration less than the model
        wb_wavelet_ricker = wb.wavelet(self.duration, self.dt, w_type=0, f=[30])
        wb_synth = wb.tuning_wedge(wb_rc, wb_wavelet_ricker)
        self.assertIsInstance(wb_synth, np.ndarray)
        self.assertEqual(wb_synth.shape, wb_rc.shape)
        # now with a wavelet with duration longer than the model
        wb_wavelet_ricker = wb.wavelet(duration=0.500, dt=self.dt, w_type=0, f=[30])
        wb_synth = wb.tuning_wedge(wb_rc, wb_wavelet_ricker)
        self.assertIsInstance(wb_synth, np.ndarray)
        self.assertEqual(wb_synth.shape[0], int(0.500 / self.dt))
        self.assertEqual(wb_synth.shape[1], wb_rc.shape[1])

    def test_10_tuning_wedge_orsmby_wavelet(self):
        wb_rc, wb_imp = wb.earth_model(self.rock_props)
        # first with a wavelet with duration less than the model
        wb_wavelet_ormsby = wb.wavelet(self.duration, self.dt, w_type=1, f=[5, 10, 40, 50])
        wb_synth = wb.tuning_wedge(wb_rc, wb_wavelet_ormsby)
        self.assertIsInstance(wb_synth, np.ndarray)
        self.assertEqual(wb_synth.shape, wb_rc.shape)
        # now with a wavelet with duration longer than the model
        wb_wavelet_ormsby = wb.wavelet(duration=0.500, dt=self.dt, w_type=1, f=[5, 10, 40, 50])
        wb_synth = wb.tuning_wedge(wb_rc, wb_wavelet_ormsby)
        self.assertIsInstance(wb_synth, np.ndarray)
        self.assertEqual(wb_synth.shape[0], int(0.500 / self.dt))
        self.assertEqual(wb_synth.shape[1], wb_rc.shape[1])

    def test_11_get_wedge_thickness(self):
        wb_rc, wb_imp = wb.earth_model(self.rock_props)
        wb_wavelet = wb.wavelet(self.duration, self.dt, w_type=0, f=[30])
        wb_synth = wb.tuning_wedge(wb_rc, wb_wavelet)
        wedge_thickness = wb.get_wedge_thickness(wb_synth, self.dt)
        self.assertIsInstance(wedge_thickness, np.ndarray)
        self.assertIsInstance(wedge_thickness.flat[0], np.int64)
        self.assertEqual(wedge_thickness.shape, (101, ))
        self.assertEqual(wedge_thickness[0], 0)
        self.assertEqual(wedge_thickness[-1], (wedge_thickness.shape[0] - 1) * self.dt * 1000)

    def test_12_get_apparent_wedge_thickness(self):
        wb_rc, wb_imp = wb.earth_model(self.rock_props)
        wb_wavelet = wb.wavelet(self.duration, self.dt, w_type=0, f=[30])
        wb_synth = wb.tuning_wedge(wb_rc, wb_wavelet)
        apparent_wedge_thickness = wb.get_apparent_wedge_thickness(wb_synth, self.dt, self.acoustic_impedance)
        self.assertIsInstance(apparent_wedge_thickness, np.ndarray)
        self.assertIsInstance(apparent_wedge_thickness.flat[0], np.int64)
        self.assertEqual(apparent_wedge_thickness.shape, (101, ))
        self.assertEqual(apparent_wedge_thickness[0], apparent_wedge_thickness[1])
        self.assertEqual(
            apparent_wedge_thickness[-1],
            (apparent_wedge_thickness.shape[0] - 1) * self.dt * 1000
        )

    def test_13_get_measured_tuning_thickness(self):
        wb_rc, _ = wb.earth_model(self.rock_props)
        wb_wavelet = wb.wavelet(self.duration, self.dt, w_type=0, f=[30])
        wb_synth = wb.tuning_wedge(wb_rc, wb_wavelet)
        measured_tuning = wb.get_measured_tuning_thickness(wb_synth, self.dt, self.acoustic_impedance)
        self.assertIsInstance(measured_tuning, float)
        self.assertGreater(measured_tuning, 0)

    def test_14_get_measured_onset_tuning_thickness(self):
        wb_rc, _ = wb.earth_model(self.rock_props)
        wb_wavelet = wb.wavelet(self.duration, self.dt, w_type=0, f=[30])
        wb_synth = wb.tuning_wedge(wb_rc, wb_wavelet)
        dz_true = wb.get_wedge_thickness(wb_synth, self.dt)
        dz_apparent = wb.get_apparent_wedge_thickness(wb_synth, self.dt, self.acoustic_impedance)
        measured_onset_tuning = wb.get_measured_onset_tuning_thickness(dz_true, dz_apparent, 30)
        self.assertIsInstance(measured_onset_tuning, int)
        self.assertGreater(measured_onset_tuning, 0)
