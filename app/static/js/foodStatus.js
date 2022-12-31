// set-Foodstatus
// load dom content event listener
document.addEventListener("DOMContentLoaded", () => {
let setFoodstatus = document.querySelectorAll("[set-foodstatus]");
// const socket = io(`https://${document.domain}:${location.port}/`);
setFoodstatus.forEach((el) => {
  try {
    let status = el.getAttribute("set-foodstatus");
    let id = el.id;
    if (status === "True") {
      el.setAttribute("checked", true);
    } else if (status === "False") {
      el.removeAttribute("checked");
    }

    el.addEventListener("change", () => {
      fetch(`https://${document.domain}:${location.port}/dashboard/edit_food_status`, {
      // fetch(`http://${document.domain}:${location.port}/edit_food_status`, {
        mode: "cors",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: id, status: el.checked }),
      });
      // socket.emit("getSuppdata", { id: id, status: el.checked });
    });
  } catch (err) {
    console.log("soceket : ", err);
  }
})
});
