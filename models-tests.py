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
           
            username='testuser',
            email='test@test.com',
            password = 'password'
        )

        db.session.add(u)
        db.session.commit()
        
        
        self.assertEqual(u.username, 'testuser')
        self.assertEqual(u.password, 'password')

    def test_sign_up(self):
        """tests our sign_up class method"""

        new_user = User.signup(username='testuser2', email='test2@test.com', password = 'password')
        db.session.commit()

        self.assertEqual(new_user.username, 'testuser2')

    def test_authenticate(self):
        """Test User Model Authenticate Method"""

        #sign member up
        other_new_user = User.signup(username='testuser3', email='test3@test.com', password = 'apassword')
        db.session.commit()
        
        # test authenticate for new person logging in
        returning_user = User.authenticate(username='testuser3', password = 'apassword')

        self.assertTrue(returning_user)


    

    
  