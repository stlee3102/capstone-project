from flask import (Flask, render_template, request, flash, session, redirect, url_for, jsonify)
from model import connect_to_db
import crud
from flask_sqlalchemy import SQLAlchemy

from jinja2 import StrictUndefined

import os
import polyline

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


MAPS_API_KEY = os.environ['GOOGLE_MAPS_KEY']

@app.route('/')
def index():
    """Show index."""

    return render_template('index.html')

@app.route('/main')
def main():

    if session.get("logged_in_user"):
        user = crud.get_user_by_email(session.get("logged_in_user"))   
        return render_template('main.html', user=user, MAPS_API_KEY = MAPS_API_KEY)

    else:
        return render_template('main.html', MAPS_API_KEY = MAPS_API_KEY)


@app.route('/register')
def show_registration():
    """Show registration form."""

    return render_template('register.html')


@app.route('/login')
def show_login():
    """Show login form."""

    return render_template('login.html')


@app.route('/admin')
def show_admin():
    """Show admin dashboard."""
    user = crud.get_user_by_email(session.get("logged_in_user"))

    return render_template('admin.html', user=user)


@app.route('/login', methods=["POST"])
def login_user():

    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if user:
        if password == user.password:
            flash(f"Successful login! Logged in {user.user_id} {user.email} {user.password}")
            session["logged_in_user"] = user.email

            if user.email == 'admin@test.com':
                return render_template('admin.html', user=user)
            else:
                return redirect(f'/main')

        else:
            flash("incorrect password, try again")
    else:
        flash("user not registered")

    return render_template('login.html')


@app.route("/logout")
def process_logout():
    """Logout User and End Session"""
    session.pop("logged_in_user")
    flash("Logged out")
    return redirect('/main')


@app.route('/users')
def show_all_users():
    
    user = crud.get_user_by_email(session.get("logged_in_user"))

    list_users = crud.return_all_users()

    return render_template('users.html', list_users=list_users, user=user)


@app.route('/users', methods=["POST"])
def register_user():
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if user:
        flash("User already created. Please login.")
        return redirect('/login')
    else:
        #create user
        crud.create_user(fname, lname, email, password)
        #automatically log in new user
        user = crud.get_user_by_email(email)
        session["logged_in_user"] = user.email
        flash("Account successfully registered")
    return redirect(f"/main")


@app.route('/users/<user_id>')
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


@app.route("/display-map-action", methods=["GET"])
def display_map_selection():
    start_pt = request.json['start_pt']
    end_pt = request.json.get['end_pt']
    mode = request.json.get['mode']
    user = crud.get_user_by_email(session.get("logged_in_user"))   

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(start_pt)
    print(end_pt)
    print(mode)
    print(user)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return render_template('display-main.html', user=user, MAPS_API_KEY=MAPS_API_KEY, start_pt=start_pt, end_pt=end_pt)


@app.route('/map-action', methods=["GET","POST"])
def map_selection():
    if request.form['trip-button'] == 'Save My Trip':
        user = crud.get_user_by_email(session.get("logged_in_user"))
        start_pt = request.form.get("start_pt")
        end_pt = request.form.get("end_pt")
        mode = request.form.get("mode")
        crud.create_map(start_pt, end_pt, mode, user.user_id)
        return redirect('/user-maps')


@app.route('/user-maps')
def show_user_maps():
    """Show a user's saved maps."""
    user = crud.get_user_by_email(session.get("logged_in_user"))

    list_maps = crud.get_maps_by_user_id(user.user_id)
    
    return render_template('maps.html', user=user, list_maps=list_maps)


@app.route('/all-maps')
def show_all_maps():
    """Show all saved maps."""

    user = crud.get_user_by_email(session.get("logged_in_user"))

    list_maps = crud.return_all_maps()

    return render_template('maps.html', user=user, list_maps=list_maps)


@app.route('/delete-map/<map_id>', methods=["GET"])
def delete_map(map_id):
    crud.delete_map(map_id)
    return redirect('/user-maps')


@app.route("/decode-polyline", methods=["POST"])
def decode_polyline():
    """Use polyline library to decode polyline string to coordinates"""
    plyline = request.json['polyline']
    coordinates = polyline.decode(plyline)
    geojson=True
    return jsonify({'coord':coordinates})


@app.route("/store-info")
def all_store_info():
    """Retrieve all store locations from db and send to map.js"""
    store_info = crud.return_all_stores() #returns list objects

    #convert list objects to dictionary to prep for jasonify
    store_dict = {}

    for store in store_info:
        store_dict[store.store_id] = {
            "name": store.name,
            "address": store.address,
            "city": store.city,
            "state": store.state,
            "zip": store.zip,
            "phone": store.phone,
            "hours": store.hours,
            "lat": store.lat,
            "long": store.long,
        }

    return jsonify({'store_info':store_dict})



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)


    
