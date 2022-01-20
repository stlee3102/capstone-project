let waypoints = [];
let markers = [];

function initMap() {
    const map = new google.maps.Map(document.getElementById("google-map"), {
        mapTypeControl: false,
        center: { lat: 37.601773,
        lng: -122.20287},
        zoom: 10,
    });

    new AutocompleteDirectionsHandler(map);

}


  
class AutocompleteDirectionsHandler {
    map;
    originPlaceId;
    destinationPlaceId;
    travelMode;
    directionsService;
    directionsRenderer;
    constructor(map) {
        this.map = map;
        this.originPlaceId = "";
        this.destinationPlaceId = "";
        this.travelMode = google.maps.TravelMode.DRIVING;
        this.directionsService = new google.maps.DirectionsService();
        this.directionsRenderer = new google.maps.DirectionsRenderer({ polylineOptions: { strokeColor: "#ff9f00" }}); //set route color to orange and render route
        this.directionsRenderer.setMap(map);  
        
        //Display text directions
        this.directionsRenderer.setPanel(document.getElementById("text-directions"));

        const originInput = document.getElementById("start_pt");
        const destinationInput = document.getElementById("end_pt");
        const modeSelector = document.getElementById("mode-selector");

        // Autocomplete origin address
        const originAutocomplete = new google.maps.places.Autocomplete(
        originInput,
        { fields: ["place_id"] }
        );

        // Autocomplete destination address
        const destinationAutocomplete = new google.maps.places.Autocomplete(
        destinationInput,
        { fields: ["place_id"] }
        );

        this.setupClickListener(
        "changemode-walking",
        google.maps.TravelMode.WALKING
        );
        this.setupClickListener(
        "changemode-bicycling",
        google.maps.TravelMode.BICYCLING
        );
        this.setupClickListener(
        "changemode-transit",
        google.maps.TravelMode.TRANSIT
        );
        this.setupClickListener(
        "changemode-driving",
        google.maps.TravelMode.DRIVING
        );
        this.setupPlaceChangedListener(originAutocomplete, "ORIG");
        this.setupPlaceChangedListener(destinationAutocomplete, "DEST");
        this.planTripListener();
    }

    // Sets a listener on a radio button to change the transportation mode
    setupClickListener(id, mode) {
        const radioButton = document.getElementById(id);

        radioButton.addEventListener("click", () => {
        this.travelMode = mode;
        });
    }

    planTripListener(){
        const planBtn = document.getElementById("plan-trip-btn");

        planBtn.addEventListener("click", () => {
            
            this.route();

            let endLocation = document.getElementById("end_pt").value;
            endLocation = endLocation.split(",");
            if (endLocation.length <= 4)
            {
                endLocation.shift();
            }
            else{
                endLocation.shift();
                endLocation.shift();
            }
            endLocation = endLocation.join(",");

            const weatherLocation = {
                location: endLocation,
            };


            fetch('/get-weather', {
                method: 'POST',
                body: JSON.stringify(weatherLocation),
                headers: {
                'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(responseJson => {
                console.log(responseJson);
                let forecast = responseJson;
                
                const forecastDiv = document.querySelector("#weather-forecast");
                forecastDiv.innerHTML = `      
                <center>       
                <h4>Destination Weather Data:</h4>
                <h6><i>
                ${forecast.location.name}, ${forecast.location.region}, ${forecast.location.country}
                </i></h6>
                </center>
                
                <p>
                <b>Local Time: </b>${forecast.location.localtime}
                <br>
                <b>Weather Data Last Updated: </b>${forecast.current.last_updated}
                </p>

                <center>
                <h3>Current Weather:</h3>
                <p>
                <img src=${forecast.current.condition.icon}>
                <br>
                ${forecast.current.condition.text}
                </center>
                <div id="weather-table">
                <b>Temp: </b>${forecast.current.temp_f}&#8457;
                <br>
                <b>Feels Like: </b>${forecast.current.feelslike_f}&#8457;
                <br>
                <b>Wind Speed: </b>${forecast.current.gust_mph} mph
                <br>
                <b>Humidity: </b>${forecast.current.humidity}
                <br>
                <b>Precipitation: </b>${forecast.current.precip_in}&#xA8;
                </div>
                </p>
                `;

                const forecastDays = forecast.forecast.forecastday;

                forecastDiv.insertAdjacentHTML("beforeend", `
                    <center>
                    <h4> Weather Forecast: </h4>
                    </center>
                `);

                for(let i=0; i <= forecastDays.length; i++)
                {
                    const weekday = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday",];
                    const d = new Date(forecastDays[i].date);
                    let convertedDay = weekday[d.getDay()];
        
                    forecastDiv.insertAdjacentHTML("beforeend", `
                
                    <center>
                    <h4>${convertedDay}</h4>
                    <h4>${forecastDays[i].date}</h4>
                    <p>
                    <img src=${forecastDays[i].day.condition.icon}>
                    <br>
                    ${forecastDays[i].day.condition.text}
                    </center>
                    <div id="weather-table">
                    <b>Max Temp: </b>${forecastDays[i].day.maxtemp_f}&#8457;
                    <br>
                    <b>Min Temp: </b>${forecastDays[i].day.mintemp_f}&#8457;
                    <br>
                    <b>Max Wind Speed: </b>${forecastDays[i].day.maxwind_mph} mph
                    <br>
                    <b>Chance of Rain: </b>${forecastDays[i].day.daily_chance_of_rain}%
                    <br>
                    <b>Chance of Snow: </b>${forecastDays[i].day.daily_chance_of_snow}%
                    <br>
                    <b>Total Precipitation: </b>${forecastDays[i].day.totalprecip_in}&#xA8;
                    </div>
                    </p>
                    `);
                }



            });
        });

    }

    setupPlaceChangedListener(autocomplete, ptType) {
        autocomplete.bindTo("bounds", this.map);
        autocomplete.addListener("place_changed", () => {
        const place = autocomplete.getPlace();

        if (!place.place_id) {
            window.alert("Please select an option from the dropdown list.");
            return;
        }

        if (ptType === "ORIG") { //setting origin
            this.originPlaceId = place.place_id;
        } else { //setting destination
            this.destinationPlaceId = place.place_id;
        }


        });
    }

    route() {
        if (!this.originPlaceId || !this.destinationPlaceId) {
        return;
        }

        const me = this;

        this.directionsService.route(
        {
            origin: { placeId: this.originPlaceId },
            destination: { placeId: this.destinationPlaceId },
            travelMode: this.travelMode,
        },
        (response, status) => {
            if (status === "OK") {

                me.directionsRenderer.setDirections(response);

                const data = {
                    polyline: response.routes[0].overview_polyline,
                };
            
                fetch('/decode-polyline', {
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: {
                    'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(responseJson => {                    
                    waypoints = responseJson.coord; //all route coordinates assigned to waypoints

                });           

                fetch('/store-info')
                .then(response => response.json())
                .then(responseJson => {                    
                    let stores = responseJson.store_info; //all store info assigned to stores
                    showStoresInBoundary(this.map, stores);
                });           
            } else {

                Toastify({
                    text: "Directions request failed due to " + status,
                    duration: 3000,
                    close: true,
                    gravity: "top", // `top` or `bottom`
                    position: "center", // `left`, `center` or `right`
                    stopOnFocus: true, // Prevents dismissing of toast on hover
                    style: {
                    background: "linear-gradient(to right, #00b09b, #96c93d)",
                    },
                }).showToast();

            }           
        }
        );
    }
}

function clearMarkers() {
    setMapOnAll(null);
    markers = [];
  } 

/****RESET MARKERS */
function showStoresInBoundary(map, stores)
{
 
    for(let i = 0; i < waypoints.length; i++)
    {
        const waypointCoordinates = [
            { lat: waypoints[i][0]-.02, lng: waypoints[i][1]-.02 },
            { lat: waypoints[i][0]-.02, lng: waypoints[i][1]+.02 },
            { lat: waypoints[i][0]+.02, lng: waypoints[i][1]+.02 },
            { lat: waypoints[i][0]+.02, lng: waypoints[i][1]-.02 },
            { lat: waypoints[i][0]-.02, lng: waypoints[i][1]-.02 },
        ];
        
        const waypointPath = new google.maps.Polyline({
            path: waypointCoordinates,
            geodesic: true,
        });

        for (let store_id in stores) {
            stores[store_id]["coords"] = {lat:stores[store_id].lat, lng:stores[store_id].long};
            storeCoord = stores[store_id].coords;
            const insideBoundary = google.maps.geometry.poly.containsLocation(storeCoord, waypointPath);

            if(insideBoundary)
            {
                const store_info_content = `Address:${stores[store_id].address}<br>`+
                `${stores[store_id].city}, ${stores[store_id].state} ${stores[store_id].zip}`+
                `<p>Phone: ${stores[store_id].phone}</p>`+
                `<p>Hours: ${stores[store_id].hours.toUpperCase()}</p>`

                markers.push(
                    new google.maps.Marker({
                        title: stores[store_id].name,
                        position: stores[store_id].coords,
                        content: store_info_content,
                        map: map,
                        icon: {
                            // custom icon
                            url: '/static/img/walmart-marker.png',
                            scaledSize: {
                              width: 25,
                              height: 40,
                            },
                          },            
                    })
                );
            }
        }    
    }

    for (const marker of markers) {
        const markerInfo = `
            ${marker.title}
            <p>
            <code>${marker.content}</code>
            </p>
            <p>
            Located at: <code>${marker.position.lat()}</code>,
            <code>${marker.position.lng()}</code>
            </p>
        `;
    
        const infoWindow = new google.maps.InfoWindow({
            content: markerInfo,
            maxWidth: 200,
        });
    
        marker.addListener('click', () => {
            infoWindow.open(map, marker);
        });
        }

}


/*
function drawBoundary(map)
{

    const waypointCoordinates = [
        { lat: waypoints[0][0]-.02, lng: waypoints[0][1]-.02 },
        { lat: waypoints[0][0]-.02, lng: waypoints[0][1]+.02 },
        { lat: waypoints[0][0]+.02, lng: waypoints[0][1]+.02 },
        { lat: waypoints[0][0]+.02, lng: waypoints[0][1]-.02 },
        { lat: waypoints[0][0]-.02, lng: waypoints[0][1]-.02 },

      ];

     const testCoord = { lat: waypoints[0][0], lng: waypoints[0][1] };

      const waypointPath = new google.maps.Polyline({
        path: waypointCoordinates,
        geodesic: true,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2,
      });
*/
      /*
      const insideBoundary = google.maps.geometry.poly.containsLocation(testCoord, waypointPath);
console.log("!!!!!!!!!!!!!!!!!!!!!");
console.log("!!!!!!!!!!!!!!!!!!!!!");

console.log(google.maps.geometry.poly.containsLocation(testCoord, waypointPath));
console.log("!!!!!!!!!!!!!!!!!!!!!");
console.log("!!!!!!!!!!!!!!!!!!!!!");

      console.log("!!!!!!!!!!!!!!!!!!!!!");
      console.log("TEST COORD:")
      console.log(testCoord);
      console.log("WAYPOINT PATH:")
      console.log(waypointPath);
      console.log("INSIDE BOUNDARY");
      console.log(insideBoundary);
      console.log("!!!!!!!!!!!!!!!!!!!!!");
*/
/*      google.maps.event.addListener(map, "click", (e) => {
          
        const resultColor = google.maps.geometry.poly.containsLocation(
          e.latLng,
          waypointPath
        )
          ? "blue"
          : "red";

        const resultPath = google.maps.geometry.poly.containsLocation(
          e.latLng,
          waypointPath
        )
          ? // A triangle.
            "m 0 -1 l 1 2 -2 0 z"
          : google.maps.SymbolPath.CIRCLE;

          

          new google.maps.Marker({
            position: e.latLng,
            map,
            icon: {
              path: resultPath,
              fillColor: resultColor,
              fillOpacity: 0.2,
              strokeColor: "white",
              strokeWeight: 0.5,
              scale: 10,
            },
          });
        });
    
      waypointPath.setMap(map);

}*/


//shows all store markers on map with infowindow of store information
/*
function showStores(map, stores)
{
    const markers = [];


    for (let store_id in stores) {
        stores[store_id]["coords"] = {lat:stores[store_id].lat, lng:stores[store_id].long};

        const store_info_content = `Address:${stores[store_id].address}<br>`+
        `${stores[store_id].city}, ${stores[store_id].state} ${stores[store_id].zip}`+
        `<p>Phone: ${stores[store_id].phone}</p>`+
        `<p>Hours: ${stores[store_id].hours.toUpperCase()}</p>`

        markers.push(
            new google.maps.Marker({
                title: stores[store_id].name,
                position: stores[store_id].coords,
                content: store_info_content,
                map: map,
             icon: {
                // custom icon
                url: '/static/img/marker.svg',
                scaledSize: {
                  width: 30,
                  height: 30,
                },
              },
            })
          );
    }

    for (const marker of markers) {
    const markerInfo = `
        ${marker.title}
        <p>
        <code>${marker.content}</code>
        </p>
        <p>
        Located at: <code>${marker.position.lat()}</code>,
        <code>${marker.position.lng()}</code>
        </p>
    `;

    const infoWindow = new google.maps.InfoWindow({
        content: markerInfo,
        maxWidth: 200,
    });

    marker.addListener('click', () => {
        infoWindow.open(map, marker);
    });
    }

}

*/