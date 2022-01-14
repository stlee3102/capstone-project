"""Automatically fill in sample user and map data"""

from model import db, User, Map, connect_to_db
from faker import Faker
import random

from server import app
connect_to_db(app)

fake = Faker()

for i in range(0,3):
    fname = fake.first_name()
    lname = fake.last_name()
    email = fake.free_email()

    user = User(fname=fname, lname=lname, email=email, password="test")

    db.session.add(user)

db.session.commit()

for j in range (0,3):
    start_pt = fake.address()
    end_pt = fake.address()
    user_id = random.randint(1,3)

    map = Map(start_pt=start_pt, end_pt=end_pt, mode = "DRIVING", user_id=user_id)
    db.session.add(map)

db.session.commit()