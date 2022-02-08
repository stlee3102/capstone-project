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
    if (qty.value >= 0 && qty.value <= 20)
    {
      let item_id = qty.name;

      fetch(`/change-item-qty/${item_id}/${qty.value}`);
    }
    else
    {
      Toastify({
        text: "Item quantity must be between 0 and 20",
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



