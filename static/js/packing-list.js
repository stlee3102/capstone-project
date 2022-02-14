for (const checkBox of document.querySelectorAll(".myCheck")) {

  checkBox.addEventListener('click', (evt) => {
    let item_id = checkBox.value; 

    const status = {
      status: checkBox.checked,
    };

    fetch(`/item/${item_id}`, {
      method: 'POST',
      body: JSON.stringify(status),
      headers: {
        'Content-Type': 'application/json',
      },
    });

  });

}

function update_item_quantity(item_id, value) {
  const quantity = {
    quantity: value,
  };

  fetch(`/item/${item_id}`, {
    method: 'POST',
    body: JSON.stringify(quantity),
    headers: {
      'Content-Type': 'application/json',
    },
  })
}

for (const qty of document.querySelectorAll("#item-qty")) {

  qty.addEventListener('click', (evt) => {
    update_item_quantity(qty.name, qty.value);
  });

  qty.addEventListener('keyup', (evt) => {
    if (qty.value >= 0 && qty.value <= 20)
    {
      update_item_quantity(qty.name, qty.value);
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



