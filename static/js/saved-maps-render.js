let waypoints = [];
let markers = [];

let originPlaceId="";
let destinationPlaceId="";


function initMap() {
    const map = new google.maps.Map(document.getElementById("google-map"), {
        mapTypeControl: false,
        center: { lat: 37.601773,
        lng: -122.20287},
        zoom: 10,
    });

    new DirectionsHandler(map);
    new WeatherHandler();
    
}

class WeatherHandler{
    constructor(){

        let endLocation = document.getElementById("endpt-id").innerText;
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
            location: endLocation
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
        <h2>Destination Weather Data</h2>
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
            <h3> Weather Forecast: </h3>
            </center>
        `);
        

        for(let i=0; i <= forecastDays.length; i++)
        {
            const weekday = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];
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
        
        })
    
    }
}
  
class DirectionsHandler {
    map;

    travelMode;
    directionsService;
    directionsRenderer;
    originInput;
    destinationInput;
    constructor(map) {
        this.map = map;

        this.originInput = document.getElementById("startpt-id").innerText;
        this.destinationInput = document.getElementById("endpt-id").innerText;
        
        var originRequest = { 
            query: this.originInput,
            fields: ["place_id"] 
        };

        var destinationRequest = {
            query: this.destinationInput,
            fields: ["place_id"] 
        };
        
        var service = new google.maps.places.PlacesService(this.map);

        service.findPlaceFromQuery(originRequest, function(results, status) {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                originPlaceId = results[0].place_id;
              
                service.findPlaceFromQuery(destinationRequest, function(results, status) {
                    if (status === google.maps.places.PlacesServiceStatus.OK) {
                        destinationPlaceId = results[0].place_id;
                    
                        if (!originPlaceId || !destinationPlaceId) {
                            return;
                        }

                        let directionsService = new google.maps.DirectionsService();
                        let travelMode = document.getElementById("mode-id").innerText;
                        travelMode = travelMode.toUpperCase();

                        let directionsRenderer = new google.maps.DirectionsRenderer({ polylineOptions: { strokeColor: "#ff9f00" }}); //set route color to orange and render route
                        directionsRenderer.setMap(map);  
        
                        //Display text directions
                        directionsRenderer.setPanel(document.getElementById("text-directions"));

                        directionsService.route(
                        {
                            origin: { placeId: originPlaceId},
                            destination: { placeId: destinationPlaceId},
                            travelMode: travelMode
                        },
                        (response, status) => {
                            if (status === "OK") {

                                directionsRenderer.setDirections(response);

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
                                    let storeCoord = stores[store_id].coords;
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
                        });           
                    } 
                    else {

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
                });
            }
        });

        }
    });
    }

    
}
