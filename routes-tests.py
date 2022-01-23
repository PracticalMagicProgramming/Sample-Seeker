"""Sample test suite for testing Sample Seeker Routes"""

# run these tests:
#
#    python -m unittest routes-tests.py

import os
from unittest import TestCase
from flask import session
from models import db
os.environ['DATABASE_URI'] = "postgresql:///smplskrredux_test"

from app import app
app.config['SQLALCHEMY_ECHO']=False
app.config['TESTING']=True




# ~~~~ QUESTIONS FOR US TO ANSWER ~~~~
# “Does this URL path map to a route function?”
# “Does this route return the right HTML?”
# “Does this route return the correct status code?”
# “After a POST to this route, are we redirected?”
# “After this route, does the DATABASE/SESSION contain expected info?”

class HomeViewTestCase(TestCase):
    """Testing our Home Route"""

    def test_get_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>SAMPLE SEEKER REDUX</h1>', html)




