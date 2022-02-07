for (const checkBox of document.querySelectorAll(".myCheck")) {

  checkBox.addEventListener('click', (evt) => {
    let item_id = checkBox.value; 

    fetch(`/change-item-status/${item_id}/${checkBox.checked}`);

  });

}

for (const qty of document.querySelectorAll("#item-qty")) {

  qty.addEventListener('click', (evt) => {
    let item_id = qty.name;

    fetch(`/change-item-qty/${item_id}/${qty.value}`);

  });

  qty.addEventListener('keyup', (evt) => {
    let item_id = qty.name;

    fetch(`/change-item-qty/${item_id}/${qty.value}`);

  });

}



