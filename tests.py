import unittest
from unittest.mock import patch, Mock
import crud
from model import connect_to_db, db, example_data
from server import app
from flask import session, jsonify, render_template
import os


class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database"""

    def setUp(self):
        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True        
        app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Drop any previous data just in case
        db.drop_all()

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    @patch('crud.db') #actions are mocked on db, actions sent to no operation(no-op) so no action actually performed on db.
    def test_create_user(self, db_mock):
        """Test create add and commit user"""
        crud.create_user(fname="Stephanie", lname="Lee", email="slee@test.com", password=b"test")

        db_mock.session.add.assert_called_once()
        db_mock.session.commit.assert_called_once()

    def test_login_function(self):
        """Test login page."""

        result = self.client.post("/login-user",
                                  data={"email": "admin@test.com", "password": "test"},
                                  follow_redirects=True)
        self.assertIn(b"Hi Admin", result.data)

    def test_not_logged_in_function(self):
        """Test main page anonymously."""

        result = self.client.get("/main",
                                  follow_redirects=True)
        self.assertIn(b"Hi there", result.data)


class FlaskTestsLoggedInAsAdmin(unittest.TestCase):
    """Flask tests that use the database when logged in as admin"""

    def setUp(self):
        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged_in_user'] = "admin@test.com"
                
        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Drop any previous data just in case
        db.drop_all()

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


    def test_logged_in_as_admin_function(self):
        """Test main page logged in as admin."""

        result = self.client.get("/main",
                                  follow_redirects=True)
        self.assertIn(b"Hi Admin", result.data)

    def test_return_all_packing_lists(self):
        """Test that all packing lists are returned for admin view"""

        result = self.client.get("/all-packing-lists")

        self.assertIn(b"Shirt", result.data)
        self.assertIn(b"Pants", result.data)
        self.assertIn(b"Vitamins", result.data)
        self.assertIn(b"Socks", result.data)
        self.assertIn(b"Dress", result.data)
        self.assertIn(b"Medicine Pills", result.data)

    def test_add_item(self):
        """Test that an item can be added to packing list"""

        result = self.client.post(
            "/item", 
            data={"user_id":1, "item-name":"Slacks", "category-name":1, "quantity":2, "status":False}, 
            follow_redirects=True
        )

        self.assertIn(b"Slacks", result.data)



if __name__ == "__main__":
    unittest.main()