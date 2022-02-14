# Roadtrippr

Roadtrippr helps you plan your next road trip by (1) helping you autocomplete addresses, (2) displaying direction timing and route data, whether you plan to walk, bike, drive, or take public transportation, (3) providing store information for all Walmart stores on route, (4) showing you destination weather data, and (5) enabling you to plan and keep track of your packing list so you know if you need to stop by a Walmart to restock supplies!

Using Google Maps JavaScript API, Google Places API, Google Directions API, and Weather API, Roadtrippr provides the ability to autocomplete origin and destination addresses, retrieve step by step direction and time to destination data, store information for all Walmart stores along the route, and destination weather data. In your account, you have the option to save and delete maps, add and delete packing list items, change the quantity of packing list items, and check off the status of whether an item has been packed yet, all of which are stored in a database. 

Users can either create an account or sign in with their Google Account, which uses the OAuth 2.0 protocol for authentication and authorization. All passwords are salted with a randomly generated 32 byte salt and hashed 100,000 times using the SHA-256 algorithm from [hashlib](https://docs.python.org/3/library/hashlib.html). A 128 byte key is generated and stored in the database along with the salt in place of the password.

The application also uses [Faker library](https://faker.readthedocs.io/en/master/) to assist in seeding an initial set of imaginary users and [Polyline API](https://pypi.org/project/polyline/#:~:text=Decoding,setting%20geojson%3DTrue) to decode coordinates from the encoded string that Google Maps API returns for route data. In addition, [Toastify](https://github.com/apvarun/toastify-js) is used to style the error notifications for Google Maps and out of bounds quantities in the Packing List. 

## Contents
* [Tech Stack](#technologies)
* [Features](#features)
* [Installation](#install)
* [Version 2.0](#version2)

## <a name="technologies"></a>Tech Stack
Backend: Python, Flask, PostgreSQL, SQLAlchemy<br/>
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3<br/>
APIs: Google Places, Google Maps JavaScript, Google Directions, Google Sign-In, Weather, Polyline<br/>
Libraries: Hashlib, Faker, Toastify<br/>

## <a name="features"></a>Features
The following is a walkthrough of the User Experience and Admin Experience:

### User Experience

The initial landing page features a JavaScript scroll animation with font opacity and font size transitions. 
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot1.gif" width="900">

The main homepage displays an interface for the user to select the origin and destination, based on autocomplete options, and the preferred mode of transportation.
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot2.png" width="900">

When the user clicks "Plan My Trip!", the app displays route timing, directions, store locations along the route, and destination weather data:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot3.png" width="900">

Users can mouseover store location markers on the map to see the store name and can click the marker to display store information:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot3a.png" width="900">

The main homepage after user account login welcomes the user by name and adds a "Save My Trip" button. The navigation bar also changes to let the user see saved maps and make a packing list:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot3b.png" width="900">

Users can register for an account to save maps and packing list information. Passwords are salted and hashed before storing in database to protect against database leaks:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot4.png" width="900">

If a user has an account already, the user can log in to the account:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot5.png" width="900">

User maps can be saved, redisplayed, and deleted:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot6.png" width="900">

Maps can be re-displayed by clicking "Display Map" without having to re-enter origin and destination information:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot7.png" width="900">

User can save item data in a packing list (item name, category, quantity, and packed status), change the quantity of an item either by changing the number directly in the quantity box or by clicking up and down arrows to increase or decrease the quantity, change the status of whether the item has been packed, and delete items from their packing list. All changes are automatically stored in the database:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot8.png" width="900">

### Admin Experience

Admin can view all user data and delete users:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot9.png" width="900">

Admin can view all users' saved maps:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot10.png" width="900">

Admin can see the encoded polyline string, decoded polyline coordinates, and test boundaries to debug map issues:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot14.png" width="900">

Admin can search weather data for any city:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot11.png" width="900">

Admin can view Weather API JSON data for debugging purposes:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot12.png" width="900">

Admin can view all users' saved packing list data, add new categories, and delete categories. Items categorized under a deleted category will be assigned to Miscellaneous. Miscellaneous category cannot be deleted.
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot13.png" width="900">

## <a name="install"></a>Installation

To run Roadtrippr:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/stlee3102/capstone-project
```

Create and activate a virtual environment inside your Roadtrippr directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip3 install -r requirements.txt
pip3 install Faker
pip3 install polyline
pip3 install requests
pip3 install Authlib
```

Sign up to use the [Weather API](https://www.weatherapi.com/docs/) and the [Google Maps APIs](https://developers.google.com/maps/documentation/javascript/overview). Make sure the Google Maps JavaScript API,  Places API, and Directions API are activated.

Obtain OAuth 2.0 credentials from the Google API Console(https://console.developers.google.com/). Authorize the following origins:
```
http://localhost
http://localhost:5000
```

Authorize the following redirect URI:
```
http://localhost:5000/authorize
```

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export GOOGLE_MAPS_KEY="YOUR_KEY_HERE"
export WEATHER_KEY="YOUR_KEY_HERE"
export GOOGLE_CLIENT_ID="YOUR_KEY_HERE"
export GOOGLE_CLIENT_SECRET="YOUR_KEY_HERE"
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up and seed 🌱 the database with sample data:

```
createdb mapdb
python -i model.py
db.create_all()
quit()
python user_map_db_filler.py
python store_db_filler.py
python packing_list_filler.py
```

Run the app:

```
python server.py
```

You can now navigate to 'localhost:5000/' to access Roadtrippr.


## <a name="version2"></a>Version 2.0
Add ability for users to:
* Save their favorite Walmart stores
* Communicate and save friends to roadtrip with together
* Text message and email their route information 