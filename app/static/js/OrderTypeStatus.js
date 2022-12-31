// dom content loaded event listener
document.addEventListener("DOMContentLoaded", () => {
  //  get surPlaceStatus EmporterStatus LivrerStatus elements
  const surPlaceStatus = document.querySelector("#surPlaceStatus");
  const EmporterStatus = document.querySelector("#EmporterStatus");
  const LivrerStatus = document.querySelector("#LivrerStatus");

  // fetch CommandType api and get data
  // fetch("http://localhost:5000/CommandType")
  fetch(`https://${document.domain}/dashboard/CommandType`)
    .then((res) => res.json())
    .then((data) => {
      // loop through data
      data.forEach((item) => {
        // check if item id is equal to 1
        if (item.id === 1) {
          // check if item is checked
          surPlaceStatus.checked = item.isCheked;
        }
        // check if item id is equal to 2
        if (item.id === 2) {
          // check if item is checked
          EmporterStatus.checked = item.isCheked;
        }
        // check if item id is equal to 3
        if (item.id === 3) {
          // check if item is checked
          LivrerStatus.checked = item.isCheked;
        }
      });
    });

  // add event listener to surPlaceStatus EmporterStatus LivrerStatus elements
  surPlaceStatus.addEventListener("click", (e) => {
    isCheked = e.target.checked;
    fetchCommandType(isCheked, 1);
  });
  EmporterStatus.addEventListener("click", (e) => {
    isCheked = e.target.checked;

    fetchCommandType(isCheked, 2);
  });
  LivrerStatus.addEventListener("click", (e) => {
    isCheked = e.target.checked;
    fetchCommandType(isCheked, 3);
  });
});

function fetchCommandType(_isCheked, _id) {
  // fetch("http://localhost:5000/CommandType", {
  fetch(`https://${document.domain}/dashboard/CommandType`, {
    
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    cors: "same-origin",
    body: JSON.stringify({ isCheked: _isCheked, id: _id }),
  }).then((res) => res.json());
}
