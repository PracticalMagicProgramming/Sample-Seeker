"""Sample test suite for testing Sample Seeker Routes"""

# run these tests:
#
#    python -m unittest login-register-tests.py

import os
from unittest import TestCase
from flask import session
from models import db
os.environ['DATABASE_URI'] = "postgresql:///smplskrredux_test"

from app import app
app.config['SQLALCHEMY_ECHO']=False
app.config['TESTING']=True



class LoginViewTestCase(TestCase):
    """Testing our Login Route"""

    def test_get_login(self):
        # get request for route
        with app.test_client() as client:
            resp = client.get('/login')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Welcome back!</h2>', html)

    def test_login_redirect(self):
        # redirect for route
        with app.test_client as client:
            resp = client.get('/login', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>SAMPLE SEEKER REDUX</h1>', html)

