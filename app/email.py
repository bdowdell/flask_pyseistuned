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

from app import mail
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender_email, sender_name, recipients, text_body, template=None):
    msg = Message(
        subject,
        sender=sender_email,
        recipients=[recipients],
        extra_headers={'name': sender_name}
    )
    #msg.body = text_body
    msg.body = render_template(
        template + '.txt',
        sender_name=sender_name,
        sender_email=sender_email,
        subject=subject,
        text_body=text_body
    )
    msg.html = render_template(
        template + '.html',
        sender_name=sender_name,
        sender_email=sender_email,
        subject=subject,
        text_body=text_body
    )
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
