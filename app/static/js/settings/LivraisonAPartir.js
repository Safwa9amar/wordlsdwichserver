// add document load dom  content event listener
document.addEventListener("DOMContentLoaded", function () {
  // get the element with id="livraisonApartir"
  let url = `${window.location.origin}/dashboard/settings/api/livraison_adresses`;
  // let url = `${window.location.origin}/settings/api/livraison_adresses`;
  let livraisonApartir = document.getElementById("livraisonApartir");
  let livraisonApartirForm = document.getElementById("livraisonApartirForm");
  let addingTarget = document.getElementById("addingTarget");

  // fetch get method to get the data and set the value of livraisonApartir

  // call the async function
  // fetchAsyncGet(url, addingTarget).then((data) => {
  //   data.forEach((item) => {
  //     let id = item.id;
  //     let val1 = item.name;
  //     let val2 = item.price;
  //     let html = addDiv(val1, val2, id, true);
  //     //   create div element
  //     let div = document.createElement("div");
  //     div.className += "form-control relative";
  //     div.innerHTML = html;
  //     addingTarget.appendChild(div);
  //   });
  // });

  // add event listener to the element
  livraisonApartir.addEventListener("click", function () {
    let html = addDiv();
    //   create div element
    let div = document.createElement("div");

    // add form-control class to div element
    div.className += "form-control relative";

    // create btn  element and add event listener
    let btn = document.createElement("button");
    btn.addEventListener("click", function () {
      div.remove();
    });
    // add btn class to btn element
    btn.className +=
      "btn btn-sm btn-outline-primary absolute left-[100%] -top-5";
    // add text to btn element
    btn.innerHTML = `
        <svg width="16" height="18" viewBox="0 0 16 18" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5.4 13.5L8 10.9L10.6 13.5L12 12.1L9.4 9.5L12 6.9L10.6 5.5L8 8.1L5.4 5.5L4 6.9L6.6 9.5L4 12.1L5.4 13.5ZM3 18C2.45 18 1.97933 17.8043 1.588 17.413C1.196 17.021 1 16.55 1 16V3H0V1H5V0H11V1H16V3H15V16C15 16.55 14.8043 17.021 14.413 17.413C14.021 17.8043 13.55 18 13 18H3ZM13 3H3V16H13V3ZM3 3V16V3Z" fill="black"/>
        </svg>
        `;
    // add btn to div element

    // add html to div element
    div.innerHTML = html;
    div.appendChild(btn);

    //   get livraisonApartirForm element
    //   add html to livraisonApartirForm element
    addingTarget.appendChild(div);
  });
  livraisonApartirForm.addEventListener("submit", function (e) {
    e.preventDefault();
    let livraisonApartir = document.getElementById("livraisonApartir");
    let livraisonApartirForm = document.getElementById("livraisonApartirForm");
    let livraisonApartirFormInputs =
      livraisonApartirForm.querySelectorAll("input:not([type='checkbox'])");
    let livraisonApartirFormInputsArray = Array.from(
      livraisonApartirFormInputs
    );
    let livraisonApartirFormInputsArrayValues =
      livraisonApartirFormInputsArray.map((input) => {
        return {
          id: input.getAttribute("attr-id"),
          val: input.value,
        };
      });
    livraisonApartir.value = livraisonApartirFormInputsArrayValues;
    // iterate over the array and create a new object with first as key and next value as value
    const formData = livraisonApartirFormInputsArrayValues
      .map((input, index) => {
        let id = input.id;
        if (index % 3 === 0) {
          let key = input;
          if (key === "" || key === undefined) return undefined;
          let value = livraisonApartirFormInputsArrayValues[index + 1];
          let value2 = livraisonApartirFormInputsArrayValues[index + 2];
          let obj = {
            id: id,
            name: key.val,
            price: value.val,
            frais_price: value2.val,
          };
          return obj;
        }

        // if (index % 2 === 0) {
        //   let key = input;
        //   if (key === "" || key === undefined) return undefined;
        //   let value = livraisonApartirFormInputsArrayValues[index + 1];
        //   let obj = {
        //     id: id,
        //     name: key.val,
        //     price: value.val,
        //   };
        //   return obj;
        // }
      })
      .filter((input) => input !== undefined);

    // fetch post method to send the data to the server
    // console.log(formData);
    // call the async function
    fetchAsyncPost(url, formData);

    // LivraisonAdressStatus element get by id
  });

  // LivraisonAdressStatus element get by id
  const LivraisonAdressStatus = document.querySelectorAll("[attr-edit]");
  // add event listener to LivraisonAdressStatus element
  LivraisonAdressStatus.forEach((item) => {
    item.addEventListener("change", function (e) {
      let id = this.getAttribute("attr-id");
      // let url = `${window.location.origin}/settings/api/livraison_adresses_status`;
      let url = `${window.location.origin}/dashboard/settings/api/livraison_adresses_status`;
      let formData = {
        id: id,
        status: this.checked,
      };
      console.log(e.target.checked);
      fetchAsyncPost(url, formData);
    });
  });
  // deleteAdress function
  // deleteAdress element get by id
  // add event listener to deleteAdress element
  // call the async function
  // call the async function
});

// Path: server\app\static\js\settings\LivraisonAPartir.js
