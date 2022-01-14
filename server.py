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


@app.route('/login', methods=["POST"])
def login_user():

    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if user:
        if password == user.password:
            flash(f"Successful login! Logged in {user.user_id} {user.email} {user.password}")
            session["logged_in_user"] = user.email
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

    list_users = crud.return_all_users()

    return render_template('users.html', list_users=list_users)


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
        user = crud.get_user_by_email(user_email)
        session["logged_in_user"] = user.email
        flash("Account successfully registered")
    return redirect(f"/main")


@app.route('/users/<user_id>')
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


@app.route('/map-action', methods=["POST"])
def map_selection():
    if request.form['trip-button'] == 'Save My Trip':
        user = crud.get_user_by_email(session.get("logged_in_user"))
        start_pt = request.form.get("start_pt")
        end_pt = request.form.get("end_pt")
        crud.create_map(start_pt, end_pt, user.user_id)
        return redirect('/user-maps')
    

@app.route('/user-maps')
def show_user_maps():
    """Show a user's saved maps."""
    user = crud.get_user_by_email(session.get("logged_in_user"))

    list_maps = crud.get_maps_by_user_id(user.user_id)
    
    return render_template('maps.html', list_maps=list_maps)


@app.route('/all-maps')
def show_all_maps():
    """Show all saved maps."""

    list_maps = crud.return_all_maps()

    return render_template('maps.html', list_maps=list_maps)


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
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(geojson)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return jsonify({'coord':coordinates})



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)


    
