# Roadtrippr
Roadtrippr helps you plan your next road trip by (1) displaying direction timing and route data, whether you plan to walk, bike, drive, or take public transportation, (2) providing store information for all Walmart stores on route so you can easily restock supplies, (3) showing you current and forecasted weather data for your destination, and (4) enabling you to plan and keep track of your packing list! 

Using Google Maps JavaScript API, Google Places API, Google Directions API, and Weather API, Roadtrippr provides autocomplete origin and destination addresses, route maps, store information, and weather data. In your account, you have the option to save and delete maps, add and delete packing list items, and check off the status of whether an item has been packed yet, all of which are stored in a database. 

The application also uses [Faker library](https://faker.readthedocs.io/en/master/) to assist in seeding user accounts with an initial set of imaginary users and [Polyline API](https://pypi.org/project/polyline/#:~:text=Decoding,setting%20geojson%3DTrue) to decode coordinates from the encoded string that Google Maps API returns for route data. In addition, [Toastify](https://github.com/apvarun/toastify-js) is used to style the Google Maps error notification. 

## Contents
* [Tech Stack](#technologies)
* [Features](#features)
* [Installation](#install)

## <a name="technologies"></a>Tech Stack
Backend: Python, Flask, PostgreSQL, SQLAlchemy<br/>
Frontend: JavaScript, AJAX, Jinja2, Bootstrap, HTML5, CSS3<br/>
APIs: Google Places, Google Maps JavaScript, Google Directions, Weather, Polyline<br/>
Libraries: Faker, Toastify<br/>

## <a name="features"></a>Features

The initial landing page features a JavaScript scroll animation with font opacity and font size transitions. 
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot1.gif" width="900">

The main homepage displays an interface for the user to select the origin and destination, based on autocomplete options, and the preferred mode of transportation.
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot2.png" width="900">

When the user clicks "Plan My Trip!", the app displays route timing, directions, store locations along the route, and destination weather data:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot3.png" width="900">

Store location pins in the map can be clicked to display store information:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot3a.png" width="900">

The main homepage after user account login welcomes the user by name and has a "Save My Trip" button:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot3b.png" width="900">

User can register for an account to save maps and packing list information:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot4.png" width="900">

If a user has an account already, the user can log in to the account:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot5.png" width="900">

User maps can be saved, redisplayed, and deleted:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot6.png" width="900">

Maps can be re-displayed without having to re-enter origin and destination information:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot7.png" width="900">

User can save item data in a packing list (item name, category, and quantity), check off whether the item has been packed, and delete items from their packing list:
<img src="https://github.com/stlee3102/capstone-project/blob/main/static/img/screenshot8.png" width="900">


Admin can:
* View all user data
* View all saved maps
* View Weather API JSON data
* Add packing list item categories
* View all packing lists

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
```

Sign up to use the [Weather API](https://www.weatherapi.com/docs/) and the [Google Maps APIs](https://developers.google.com/maps/documentation/javascript/overview). Make sure the Google Maps JavaScript API,  Places API, and Directions API are activated.

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export GOOGLE_MAPS_KEY="YOUR_KEY_HERE"
export WEATHER_KEY="YOUR_KEY_HERE"
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