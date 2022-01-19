displayTripListener();

function displayTripListener(){

    const formInputs = {
        start_pt: document.querySelector('#start-pt-id').innerHTML,
        end_pt: document.querySelector('#end-pt-id').innerHTML,
        mode: document.querySelector('#mode-id').innerHTML,
      };
    

    const displayBtn = document.querySelector('#display-btn');

    displayBtn.addEventListener("click", () => {
        
        fetch('/display-map-action', {
            method: 'GET',
            body: JSON.stringify(formInputs),
            headers: {
              'Content-Type': 'application/json',
            },
          });


        });

}


