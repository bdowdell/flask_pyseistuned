#!/usr/bin/env python

import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dont-panic42'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 8025))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    PST_MAIL_SENDER = 'PySeisTuned Admin <admin@pyseistuned.com>'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['ben@test.com']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    ADMINS = [os.environ.get('PST_ADMIN')]

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to administrator
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.PST_MAIL_SENDER,
            toaddrs=cls.ADMINS,
            subject='PySeisTuned Application Error',
            credentials=credentials,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'unix': UnixConfig,
    'default': DevelopmentConfig,
}
