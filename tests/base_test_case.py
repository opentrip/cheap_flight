# coding: utf-8

from flask.ext.testing import TestCase
from cheapflight.app import create_app
from cheapflight.ext import db

from cheapflight.config import TestingConfig


class BaseTestCase(TestCase):

    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass


__all__ = ["BaseTestCase"]
