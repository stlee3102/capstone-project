displayTripListener();

function displayTripListener(){
  
    const cardGrid = document.getElementById("card-grid");

    for (card of cardGrid.children) {
        const displayBtn = card.querySelector("#display-btn");
     
        displayBtn.addEventListener("click", (event) => {
            
            cardBody = event.target.parentNode.parentNode;
        
            window.location.href = '/display-map-action?' + new URLSearchParams({
                start_pt: cardBody.querySelector('#start-pt-id').innerHTML,
                end_pt: cardBody.querySelector('#end-pt-id').innerHTML,
                mode: cardBody.querySelector("#mode-id").innerHTML,
            });


        })
    }
}


//    console.log(mode)




//        if (mode == 'Driving')
  //          $("#changemode-driving").prop("checked", true);

          /*  <input type="radio" name="mode" id="changemode-walking" value="Walking"/>
            <label for="changemode-walking">Walking</label>

            <input type="radio" name="mode" id="changemode-bicycling" value="Bicycling"/>
            <label for="changemode-bicycling">Bicycling</label>

            <input type="radio" name="mode" id="changemode-transit" value="Transit"/>
            <label for="changemode-transit">Transit</label>
    
            <input type="radio" name="mode" id="changemode-driving" value="Driving"/>
            <label for="changemode-driving">Driving</label>
*/
        
        /*
        fetch('/display-map-action?' + new URLSearchParams({
            start_pt: document.querySelector('#start-pt-id').innerHTML,
            end_pt: document.querySelector('#end-pt-id').innerHTML,
            mode: document.querySelector('#mode-id').innerHTML
        })).then(function (response) {
            // The API call was successful!
            return response.text();
        }).then(function (html) {
            document.body.innerHTML = html 
        
        }).catch(function (err) {
            // There was an error
            console.warn('Something went wrong.', err);
        });
        */
 

