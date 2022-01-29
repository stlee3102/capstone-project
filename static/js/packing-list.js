for (const checkBox of document.querySelectorAll(".myCheck")) {

    checkBox.addEventListener('click', (evt) => {
    let item_id = checkBox.value; 

    fetch(`/change-item-status/${item_id}/${checkBox.checked}`);

  });

}
