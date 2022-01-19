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
