document.addEventListener("DOMContentLoaded", function () {
  // // let url = `${window.location.origin}/settings/api/faris`;
  // let url = `${window.location.origin}/dashboard/settings/api/faris`;
  // let livraisonPrix = document.getElementById("livraisonPrix");
  // // asyc and await fetch get method
  // async function fetchAsync() {
  //   const response = await fetch(url, {
  //     method: "GET",
  //     headers: {
  //       "Content-Type": "application/json",
  //     },
  //   });
  //   const data = await response.json();
  //   return data;
  // }
  // // call the async function
  // fetchAsync().then((data) => {
  //   livraisonPrix.value = data[0].price;
  // });

  //   // asyc and await fetch post method
  // livraisonPrix.addEventListener("change", function (e) {
  //   let val = e.target.value;
  //   // asyc and await fetch
  //   async function fetchAsync() {
  //     const response = await fetch(url, {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({ livraisonPrix: val }),
  //     });
  //     const data = await response.json();
  //     return data;
  //   }
  //   // call the async function
  //   fetchAsync().then((data) => console.log(data));
  // });

  // clientStatus element get by id and add event listener 
  const clientStatus = document.getElementById("clientStatus");
  clientStatus.addEventListener("change", function (e) {
    // let url = `${window.location.origin}/dashboard/settings/api/client_status`;
    let url = `${window.location.origin}/settings/api/client_status`;
    let formData = {
      status: this.checked,
    };
    fetchAsyncPost(url, formData);
  });
  
});
