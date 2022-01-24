"""Sample test suite for testing Sample Seeker Routes"""

# run these tests:
#
#    python -m unittest login-register-tests.py

import os
from unittest import TestCase
from flask import session
from models import db, User
from flask_login import LoginManager, login_required, login_user, logout_user
os.environ['DATABASE_URI'] = "postgresql:///smplskrredux_test"

from app import app
app.config['SQLALCHEMY_ECHO']=False
app.config['TESTING']=True



class LoginViewTestCase(TestCase):
    """Testing our Login Route"""
    
    def setUp(self):
        """Make demo data commmit it to our testing database, clean up altered data from last test"""

    # instantiate user data to be used by the tests
        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser")
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("abc", "test1@test.com", "password")
        self.u1_id = 778
        self.u1.id = self.u1_id
        self.u2 = User.signup("efg", "test2@test.com", "password")
        self.u2_id = 884
        self.u2.id = self.u2_id
        self.u3 = User.signup("hij", "test3@test.com", "password")
        self.u4 = User.signup("testing", "test4@test.com", "password")
        

    def tearDown(self):
        """Clean up fouled transactions."""
        resp = super().tearDown()
        db.session.rollback()
        return resp
    def test_get_login(self):
        # get request for route
        with app.test_client() as client:
            resp = client.get('/login')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Welcome back!</h2>', html)

    def test_login_redirect(self):
        # redirect for route
        with app.test_client() as client:
            resp = client.get('/login', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
         

