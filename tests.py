import unittest
from unittest.mock import patch, Mock
import crud
from model import connect_to_db, db, example_data
from server import app
from flask import session, jsonify, render_template
import os


############# UNIT TESTS #############

#mock database
@patch('crud.db')
def test_create_user(db_mock):
    crud.create_user(fname="Stephanie", lname="Lee", email="slee@test.com", password="test")

    db_mock.session.add.assert_called_once()
    db_mock.session.commit.assert_called_once()

############# INTEGRATION TESTS #############

class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database"""

    def setUp(self):
        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

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

    def test_login_function(self):
        """Test login page."""

        result = self.client.post("/login-user",
                                  data={"email": "admin@test.com", "password": "test"},
                                  follow_redirects=True)
        self.assertIn(b"Hi Admin", result.data)


class FlaskTestsLoggedInAsAdmin(unittest.TestCase):
    """Flask tests that use the database when logged in as admin"""

    def setUp(self):
        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

        with self.client as u:
            with u.session_transaction() as sess:
                sess['user'] = "admin@test.com"
                sess['user_id'] = 1

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

        result.self.client.get("/add-item")
        self.assertIn()
        crud.add_item(user_id=2, item_name="Slacks", category_name=1, quantity=2, status=False)




#     user = crud.get_user_by_email(session.get("logged_in_user"))

#     item_name = request.args.get('item-name', '')
#     category_name = request.args.get('category-name', '')
#     quantity = request.args.get('quantity', '')
#     status = request.args.get('status', '') in ('true', 'True', 'TRUE') #boolean check of status string

#     user = crud.get_user_by_email(session.get("logged_in_user"))

#     crud.add_item(user_id=user.user_id, item_name=item_name, category_name=category_name, quantity=quantity, status=status)

#     if user.email == 'admin@test.com':
#         return redirect('/all-packing-lists')
#     else:
#         return redirect('/packing-list')

if __name__ == "__main__":
    unittest.main()