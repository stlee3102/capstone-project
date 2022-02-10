let waypoints = [];


function initMap() {

    //set initial default map coordinate information
    const map = new google.maps.Map(document.getElementById("show-boundary"), {
        mapTypeControl: false,
        center: { lat: 37.601773,
        lng: -122.20287},
        zoom: 15,
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
        this.directionsRenderer.setMap(map);  //set map to initial preset coordinates from map constant
        
        //Display text directions
        this.directionsRenderer.setPanel(document.getElementById("text-directions"));

        const originInput = document.getElementById("start_pt"); //get origin
        const destinationInput = document.getElementById("end_pt"); //get destination
        const modeSelector = document.getElementById("mode-selector"); //get travel mode

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

        //set up listeners for travel modes
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

        //set up listeners for origin and destination
        this.setupPlaceChangedListener(originAutocomplete, "ORIG");
        this.setupPlaceChangedListener(destinationAutocomplete, "DEST");

        //sets up listener for when user hits plan trip button to provide directions and weather forecast information
        this.planTripListener();
    }

    // Sets a listener on a radio button to change the transportation mode
    setupClickListener(id, mode) {
        const radioButton = document.getElementById(id);

        radioButton.addEventListener("click", () => {
        this.travelMode = mode;
        });
    }
    
    //Sets a listener on the autocomplete address bars to set the origin and destination as user selects addresses
    setupPlaceChangedListener(autocomplete, ptType) {
        autocomplete.bindTo("bounds", this.map);
        autocomplete.addListener("place_changed", () => {
        const place = autocomplete.getPlace();

        if (!place.place_id) {

            Toastify({
                text: "Please select an option from the dropdown list.",
                duration: 3000,
                close: true,
                gravity: "top", // `top` or `bottom`
                position: "center", // `left`, `center` or `right`
                stopOnFocus: true, // Prevents dismissing of toast on hover
                style: {
                background: "linear-gradient(to right, #00b09b, #96c93d)",
                },
            }).showToast();

            return;
        }

        if (ptType === "ORIG") { //setting origin
            this.originPlaceId = place.place_id;
        } else { //setting destination
            this.destinationPlaceId = place.place_id;
        }
        });
    }

    //Sets up a listener on plan trip button to provide directions and weather forecast information when user clicks plan trip button
    planTripListener(){
        const planBtn = document.getElementById("plan-trip-btn");

        planBtn.addEventListener("click", () => {
            
            document.body.style.overflowY = "visible"; //turn off overflow-Y:hidden in CSS

            this.route(); //call function to get route information            
            

        });

    }


    //calculate route information and display markers for store locations within boundaries
    route() {

        //if origin or destination are missing, return none
        if (!this.originPlaceId || !this.destinationPlaceId) {
            return;
        }

        const me = this;

        //get waypoints 
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
                    polyline: response.routes[0].overview_polyline, //returns encoded string from Google API
                };

                document.getElementById("polyline-string").innerText = response.routes[0].overview_polyline;
            
                //send encoded string to server to decode polyline
                fetch('/decode-polyline', {
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: {
                    'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(responseJson => {                    
                    waypoints = responseJson.coord; //receive decoded polyline as a list of coordinate lists and assign all route coordinates to waypoints variable
                    document.getElementById("route-coordinates").innerText = waypoints;

                    drawBoundary(this.map);

                                                    
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




//use to show boundary lines for testing purposes

function drawBoundary(map)
{

    const waypointCoordinates = [
        { lat: waypoints[0][0]-.04, lng: waypoints[0][1]-.04 },
        { lat: waypoints[0][0]-.04, lng: waypoints[0][1]+.04 },
        { lat: waypoints[0][0]+.04, lng: waypoints[0][1]+.04 },
        { lat: waypoints[0][0]+.04, lng: waypoints[0][1]-.04 },
        { lat: waypoints[0][0]-.04, lng: waypoints[0][1]-.04 },

      ];

     const testCoord = { lat: waypoints[0][0], lng: waypoints[0][1] };

      const waypointPath = new google.maps.Polyline({
        path: waypointCoordinates,
        geodesic: true,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2,
      });

    const insideBoundary = google.maps.geometry.poly.containsLocation(testCoord, waypointPath);

      google.maps.event.addListener(map, "click", (e) => {
          
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
              fillOpacity: 0.8,
              strokeColor: "white",
              strokeWeight: 0.5,
              scale: 10,
            },
          });
        });
    
      waypointPath.setMap(map);

}
