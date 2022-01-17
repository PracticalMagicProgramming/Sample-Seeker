"""User model tests."""

# run these tests like:
#
#    python -m unittest models-tests.py


import os
from unittest import TestCase

from models import db, User

os.environ['DATABASE_URI'] = "postgresql:///smplskrredux_test"


from app import app
app.config['SQLALCHEMY_ECHO']=False
app.config['TESTING']=True



class ModelTestCase(TestCase):
    """Testing our SQLA Models"""
    
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()
        
    def setUp(self):
        """Clear models and add sample data."""

        User.query.delete()
        db.session.commit()

    def tearDown(self):
        """clearing session after each test"""

        db.session.rollback()
        

    def test_user_model(self):
        """Adding to User Model"""

        u = User(
            email='test@test.com',
            username='testuser',
        )

        db.session.add(u)
        db.session.commit()
        
        
        self.assertEqual(u.username, 'testuser')
    

    
  