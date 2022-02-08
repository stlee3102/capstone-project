from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
from model import connect_to_db
import crud
from flask_sqlalchemy import SQLAlchemy
from pprint import pformat
from jinja2 import StrictUndefined

import hashlib # for password hashing
import os # for API keys and password hashing
import polyline # for decoding Google Maps encoded route coordinate string
import requests # for API

from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

MAPS_API_KEY = os.environ['GOOGLE_MAPS_KEY']
WEATHER_API_KEY = os.environ['WEATHER_KEY']


#Create Salted and Hashed Password
def create_hashed_password(password):
    """Create salted and hashed password. Returns binary containing salt and key."""
    salt = os.urandom(32) #32 byte

    key = hashlib.pbkdf2_hmac(
        'sha256', # the hash digest algorithm for HMAC
        password.encode('utf-8'), # convert the password to bytes
        salt,
        100000, # 100k iterations of SHA-256
        dklen=128 # get 128 byte key
    )

    storage = salt + key #set variable to store salt and key together for password

    return storage


def get_hashed_password(salt, password):
    """Get hashed password from salt and attempted password. Returns binary containing only key."""

    key = hashlib.pbkdf2_hmac(
        'sha256', # the hash digest algorithm for HMAC
        password.encode('utf-8'), # convert the password to bytes
        salt,
        100000, # 100k iterations of SHA-256
        dklen=128 # get 128 byte key
    )

    return key


#Google OAuth setup
oauth = OAuth(app)
google = oauth.register(
name="google",
client_id=os.environ["GOOGLE_CLIENT_ID"],
client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
access_token_url="https://accounts.google.com/o/oauth2/token",
access_token_params=None,
authorize_url="https://accounts.google.com/o/oauth2/auth",
authorize_params=None,
api_base_url="https://www.googleapis.com/oauth2/v1/",
client_kwargs={"scope": "openid profile email"}
)

@app.route("/google-login")
def login():
    google = oauth.create_client("google")
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/authorize")
def authorize():
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    resp = google.get("userinfo")
    resp.raise_for_status()
    profile = resp.json()
    
    if crud.get_user_by_email(profile["email"]):
        user = crud.get_user_by_email(profile["email"])
        session["logged_in_user"] = user.email
    else:
        password = create_hashed_password(profile["id"])

        crud.create_user(profile["given_name"], profile["family_name"], profile["email"], password)
        user = crud.get_user_by_email(profile["email"])
        session["logged_in_user"] = user.email
    return redirect("/main")



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
    """Show login form"""

    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login_user():
    """Login User"""

    email = request.form.get("email")
    attempted_password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if user:            
        salt_from_storage = user.password[:32] #extract salt from stored password
        key_from_storage = user.password[32:] #extract key from stored password

        #hash attempted password
        attempted_key = get_hashed_password(salt_from_storage, attempted_password)
 
        if attempted_key == key_from_storage:
            # flash(f"Successful login!")
            session["logged_in_user"] = user.email

            if user.email == 'admin@test.com':
                return render_template('admin.html', user=user)
            else:
                return redirect(f'/main')
        else:
            flash("Incorrect password, try again")
    else:
        flash("User not registered")

    return render_template('login.html')


@app.route("/logout")
def process_logout():
    """Logout User and End Session"""
    session.pop("logged_in_user")
    # flash("Logged out")
    return redirect('/main')


@app.route('/admin')
def show_admin():
    """Show admin dashboard."""
    user = crud.get_user_by_email(session.get("logged_in_user"))

    return render_template('admin.html', user=user)


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
        hashed_password = create_hashed_password(password)
        
        #create user
        crud.create_user(fname, lname, email, hashed_password)
        #automatically log in new user
        user = crud.get_user_by_email(email)
        session["logged_in_user"] = user.email
        # flash("Account successfully registered")
    return redirect(f"/main")


@app.route('/users/<user_id>')
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


@app.route("/display-map-action", methods=["GET"])
def display_map_selection():
    start_pt = request.args['start_pt']
    end_pt = request.args['end_pt']
    mode = request.args['mode']
    user = crud.get_user_by_email(session.get("logged_in_user"))   

    return render_template('display-main.html', user=user, MAPS_API_KEY=MAPS_API_KEY, start_pt=start_pt, end_pt=end_pt, mode=mode)


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

@app.route("/get-weather", methods=["POST"])
def get_weather():
    location = request.json['location']

    url = 'http://api.weatherapi.com/v1/forecast.json'
    payload = {'key': WEATHER_API_KEY}

    payload['q'] = location
    payload['days'] = 3

    res = requests.get(url, params=payload)

    data = res.json()

    return data  
    

@app.route('/weather')
def show_weather_form():
    """Show weather search form"""

    user = crud.get_user_by_email(session.get("logged_in_user"))


    return render_template('search-form.html', user=user)


@app.route('/weather/search')
def find_weather():
    """Search Weather API for Admin Dashboard"""

    q = request.args.get('q', '')
    days = request.args.get('days', '')


    url = 'http://api.weatherapi.com/v1/forecast.json'
    payload = {'key': WEATHER_API_KEY}

    payload['q'] = q
    payload['days'] = days

    res = requests.get(url, params=payload)

    data = res.json()

    location = data['location']
    current = data['current']
    forecastdays = data['forecast']['forecastday']

    user = crud.get_user_by_email(session.get("logged_in_user"))


    return render_template('search-results.html',
                            pformat=pformat, forecastdays=forecastdays,
                           data=data, user=user, location=location, current=current)


@app.route('/packing-list')
def show_packing_list():
    """Show a user's packing list"""

    user = crud.get_user_by_email(session.get("logged_in_user"))
    packinglist = crud.get_packing_list_by_user_id(user.user_id)
    categories = crud.get_categories()

    return render_template('packinglist.html', user=user, packinglist=packinglist, categories=categories)


@app.route('/all-packing-lists')
def show_all_packing_lists():
    """Show all packing lists"""

    user = crud.get_user_by_email(session.get("logged_in_user"))

    packinglist = crud.return_all_packing_lists()
    categories = crud.get_categories()

    return render_template('packinglist.html', user=user, packinglist=packinglist, categories=categories)


@app.route('/add-category')
def add_category():
    """Add Category to Packing List"""

    category_name = request.args.get('category-name', '')

    crud.add_category(category_name=category_name)

    return redirect('/packing-list')


@app.route('/delete-category')
def delete_category():
    """Delete Category to Packing List"""

    category_name = request.args.get('category-name', '')

    if category_name != "Miscellaneous":
        crud.delete_category(category_name=category_name)
    else:
        flash("Miscellaneous Category Deletion Not Permitted")
    
    return redirect('/packing-list')


@app.route('/add-item')
def add_item():
    """Add Item to Packing List"""

    item_name = request.args.get('item-name', '')
    category_name = request.args.get('category-name', '')
    quantity = request.args.get('quantity', '')
    status = request.args.get('status', '') in ('true', 'True', 'TRUE') #boolean check of status string

    user = crud.get_user_by_email(session.get("logged_in_user"))

    crud.add_item(user_id=user.user_id, item_name=item_name, category_name=category_name, quantity=quantity, status=status)

    return redirect('/packing-list')

@app.route('/delete-item/<item_id>', methods=["GET"])
def delete_item(item_id):
    """"Delete Item from Packing List"""

    crud.delete_item(item_id)

    return redirect('/packing-list')

@app.route('/change-item-status/<item_id>/<status>')
def change_item_status(item_id, status):
    """Change Status of Item in Packing List"""

    crud.change_item_status(item_id=item_id, status=status)
    
    return redirect('/packing-list')


@app.route('/change-item-qty/<item_id>/<qty>')
def change_item_qty(item_id, qty):
    """Change Quantity of Item in Packing List"""

    crud.change_item_qty(item_id=item_id, qty=qty)
    
    return redirect('/packing-list')


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)