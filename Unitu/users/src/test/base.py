from flask_testing import TestCase
from flask import current_app

from src import create_app

import requests
import json

from src.test.utils_test import reset_all_rows

app = create_app()

class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('src.config.Config')
        return app

    def stupidSideEffect(self, *args, **kwargs):
        raise ValueError("error message test")

    def setUp(self):
        reset_all_rows()

    def tearDown(self):
        reset_all_rows()
