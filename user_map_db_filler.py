"""Automatically fill in sample user and map data"""

from model import db, User, Map, connect_to_db
from random_address import real_random_address
from faker import Faker
import random
import random_address

import hashlib
import os

from server import app
connect_to_db(app)

fake = Faker()

#make 3 maps each time run
def make_maps(id):

    user_id = id

    for j in range (0,3):
        start_pt_gen = random_address.real_random_address_by_state('CA')
        start_pt = start_pt_gen["address1"]+", "+start_pt_gen["city"]+", "+start_pt_gen["state"]+" "+start_pt_gen["postalCode"]

        end_pt_gen = random_address.real_random_address_by_state('CA')
        end_pt = end_pt_gen["address1"]+", "+end_pt_gen["city"]+", "+end_pt_gen["state"]+" "+end_pt_gen["postalCode"]

        map = Map(start_pt=start_pt, end_pt=end_pt, mode = "Driving", user_id=user_id)

        db.session.add(map)
        db.session.commit()

#make test hashed password
def make_pwd():
    password = "test" #same password for all test users

    salt = os.urandom(32) #randomly generate a 32 byte salt

    key = hashlib.pbkdf2_hmac(
        'sha256', # the hash digest algorithm for HMAC
        password.encode('utf-8'), # convert the password to bytes
        salt,
        100000, # 100k iterations of SHA-256
        dklen=128 # get 128 byte key
    )

    storage = salt + key #set variable to store salt and key together for password

    return storage

#make admin account

password = make_pwd()

user = User(fname="Admin", lname="Test", email="admin@test.com", password=password)
db.session.add(user)
db.session.commit()
make_maps(1)

#make default user test account
password = make_pwd()

user = User(fname="Jane", lname="Smith", email="jane@test.com", password=password)
db.session.add(user)
db.session.commit()
make_maps(2)

#make other user accounts

for i in range(0,2):
    fname = fake.first_name()
    lname = fake.last_name()

    email = fname[0:1]+lname+"@test.com";
    email = email.lower();

    password = make_pwd()

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)

    db.session.commit()

    id = i+3 #make user id's start at 3 since the first two users area reserved for Admin and Jane

    make_maps(id) #make maps for each user id