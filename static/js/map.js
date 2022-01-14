let waypoints = [];

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
        this.directionsRenderer = new google.maps.DirectionsRenderer();
        this.directionsRenderer.setMap(map);  
        
        
        //Display text directions
        this.directionsRenderer.setPanel(document.getElementById("sidebar"))

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
            });

    }

    setupPlaceChangedListener(autocomplete, mode) {
        autocomplete.bindTo("bounds", this.map);
        autocomplete.addListener("place_changed", () => {
        const place = autocomplete.getPlace();

        if (!place.place_id) {
            window.alert("Please select an option from the dropdown list.");
            return;
        }

        if (mode === "ORIG") { //setting origin
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

                    document.querySelector('#debug').insertAdjacentHTML(
                        'beforeend',
                        
                        ` <li>${waypoints}</li>`,
                      );

                });           
            } else {
            window.alert("Directions request failed due to " + status);
            }

           
        }
        );
    }
}

