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

import unittest
from app import create_app
from app.main.forms import ContactForm, TuningWedgeForm


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.soft_ricker_wedge_form = TuningWedgeForm(
            layer_1_vp=3000, layer_1_dens=2.5, layer_1_impedance=7500,
            layer_2_vp=2700, layer_2_dens=2.3, layer_2_impedance=6210,
            vp_units=0, wv_type=0, frequency='25',
            wv_length=0.200, wv_dt=0.001
        )
        self.soft_ormsby_wedge_form = TuningWedgeForm(
            layer_1_vp=3000, layer_1_dens=2.5, layer_1_impedance=7500,
            layer_2_vp=2700, layer_2_dens=2.3, layer_2_impedance=6210,
            vp_units=0, wv_type=1, frequency='5, 10, 40, 50',
            wv_length=0.200, wv_dt=0.001
        )

    def tearDown(self):
        self.app_context.pop()

    def test_index_page_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_page_post_ricker(self):
        # Ricker Wavelet
        response = self.client.post('/index', data=self.soft_ricker_wedge_form.data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/index', data=self.soft_ricker_wedge_form.data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.soft_ricker_wedge_form.validate())

    def test_index_page_post_ormsby(self):
        # Ormsby Wavelet
        response = self.client.post('/index', data=self.soft_ormsby_wedge_form.data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/index', data=self.soft_ormsby_wedge_form.data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.soft_ormsby_wedge_form.validate())

    def test_index_page_post_same_impedance(self):
        form = self.soft_ricker_wedge_form
        form.layer_2_vp.data = form.layer_1_vp.data
        form.layer_2_dens.data = form.layer_1_dens.data
        form.layer_2_impedance.data = form.layer_1_impedance.data
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)  # form should not validate
        self.assertFalse(form.validate())

    def test_index_page_post_bad_velocity(self):
        # layer_1_vp is empty
        form = self.soft_ricker_wedge_form
        form.layer_1_vp.data = ''
        response = self.client.post('/index', data=dict(layer_1_vp=''))
        self.assertEqual(response.status_code, 200)  # form should not validate
        self.assertFalse(form.validate())
        # layer_1_vp is negative
        form.layer_1_vp.data = -3000
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)  # form should not validate
        self.assertFalse(form.validate())
        # layer_1_vp is > 20000
        form.layer_1_vp.data = 100000
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)  # should not validate
        self.assertFalse(form.validate())
        # layer_1_vp is non-numeric
        form.layer_1_vp.data = 'apple'
        response = self.client.post('/index', data=dict(layer_1_vp='apple'))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(TypeError):
            form.validate()

    def test_index_page_post_bad_density(self):
        # layer_1_dens is missing
        form = self.soft_ricker_wedge_form
        form.layer_1_dens.data = ''
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)  # form should not validate nor follow redirect
        self.assertFalse(form.validate())
        # layer_1_dens below minimum 1.0
        form.layer_1_dens.data = 0.9
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.validate())
        # layer_1_dens above maximum 5.0
        form.layer_1_dens.data = 5.1
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.validate())
        # layer_1_dens is non-numeric
        form.layer_1_dens.data = 'apple'
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(TypeError):
            form.validate()

    def test_index_page_post_bad_ricker_num_freqs(self):
        # Ricker wavelet too many frequencies
        form = self.soft_ricker_wedge_form
        form.frequency.data = '30, 20'
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.validate())

    def test_index_page_post_bad_ricker_neg_freqs(self):
        # Ricker wavelet f_central < 0:
        form = self.soft_ricker_wedge_form
        form.frequency.data = '-30'
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.validate())

    def test_index_page_post_bad_ormsby_bad_sep(self):
        # Ormsby wavelet frequencies not comma separated
        form = self.soft_ormsby_wedge_form
        form.frequency.data = '5 10 15 20'
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.validate())

    def test_index_page_post_bad_orsmby_num_freqs(self):
        # Ormsby wavelet number of frequencies != 4
        form = self.soft_ormsby_wedge_form
        form.frequency.data = '5, 10, 20, 30, 40'
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.validate())
        form.frequency = '5, 10, 20'
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.validate())

    def test_index_page_post_bad_ormsby_neg_freqs(self):
        # Ormsby wavelet with negatives frequencies
        form = self.soft_ormsby_wedge_form
        form.frequency.data = '10, -20, 30, -40'
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.validate())

    def test_index_page_post_bad_ormsby_freqs_not_sequential(self):
        # Ormsby wavelet frequencies not sequentially ordered from least to greatest
        form = self.soft_ormsby_wedge_form
        form.frequency.data = '30, 10, 40, 20'
        response = self.client.post('/index', data=form.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.validate())

    def test_about_page_get(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_contact_page_get(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)

    def test_contact_page_post(self):
        form = ContactForm(
            name='Test Name',
            email='test@mail.com',
            subject='Hello World',
            body='Is there anybody out there?'
        )
        response = self.client.post('/contact', data=form.data)
        self.assertEqual(response.status_code, 302)  # successful validation should result in redirect
        response = self.client.post('/contact', data=form.data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.validate())

    def test_contact_page_bad_name_field(self):
        form = ContactForm(
            name=None,
            email='test@mail.com',
            subject='Hello World',
            body='This should not validate'
        )
        response = self.client.post('/contact', data=form.data)
        self.assertIsNot(form.validate(), True)  # name is required to validate
        self.assertEqual(response.status_code, 200)

    def test_contact_page_bad_email_field(self):
        form = ContactForm(
            name='Test Name',
            email='test@mail',
            subject='Hello World',
            body='This should not validate'
        )
        response = self.client.post('/contact', data=form.data)
        self.assertIsNot(form.validate(), True)  # email is not valid
        self.assertEqual(response.status_code, 200)

    def test_contact_page_bad_subject_field(self):
        form = ContactForm(
            name='Test Name',
            email='test@mail.com',
            subject=None,
            body='This should not validate'
        )
        response = self.client.post('/contact', data=form.data)
        self.assertIsNot(form.validate(), True)  # subject is required to validate
        self.assertEqual(response.status_code, 200)

    def test_contact_page_bad_body_field(self):
        form = ContactForm(
            name='Test Name',
            email='test@mail.com',
            subject='Hello World',
            body=None
        )
        response = self.client.post('/contact', data=form.data)
        self.assertIsNot(form.validate(), True)  # body is required to validate
        self.assertEqual(response.status_code, 200)
        form = ContactForm(
            name='Test Name',
            email='test@mail.com',
            subject='Hello World',
            body='a'
        )
        response = self.client.post('/contact', data=form.data)
        self.assertIsNot(form.validate(), True)  # body should be too short to validate
        self.assertEqual(response.status_code, 200)

    def test_success_page_get(self):
        response = self.client.get('/success')
        self.assertEqual(response.status_code, 200)

    def test_404(self):
        response = self.client.get('/bad-url')
        self.assertEqual(response.status_code, 404)
        
    def test_forms_NotEqualTo_bad_field(self):
        form = self.soft_ricker_wedge_form
        form.layer_2_dens.data = form.layer_1_dens.data
        from app.main.forms import NotEqualTo
        self.assertFalse(form.layer_2_dens.validate(form=form, extra_validators=[NotEqualTo('dens1')]))

    def test_forms_NotEqualTo_no_message(self):
        form = self.soft_ricker_wedge_form
        form.layer_2_dens.data = form.layer_1_dens.data
        from app.main.forms import NotEqualTo
        self.assertFalse(form.layer_2_dens.validate(
            form=form,
            extra_validators=[NotEqualTo('layer_1_dens')]
        ))

    def test_forms_ValidateFrequency_bad_field(self):
        form = self.soft_ricker_wedge_form
        from app.main.forms import ValidateFrequency
        self.assertFalse(form.frequency.validate(
            form=form,
            extra_validators=[ValidateFrequency('wv')]
        ))

    def test_forms_ValidateFrequency_ormsby_no_message(self):
        form = self.soft_ormsby_wedge_form
        form.frequency.data = 10
        from app.main.forms import ValidateFrequency
        with self.assertRaises(AttributeError):
            form.frequency.validate(form=form, extra_validators=[ValidateFrequency('wv_type')])

    def test_forms_ValidateFrequency_ricker_no_message(self):
        form = self.soft_ricker_wedge_form
        form.frequency.data = 10
        from app.main.forms import ValidateFrequency
        with self.assertRaises(AttributeError):
            form.frequency.validate(form=form, extra_validators=[ValidateFrequency('wv_type')])
