// dom content load event listener
document.addEventListener("DOMContentLoaded", () => {
    let url = `${window.location.origin}/dashboard/settings/api/notification`;
    // let url = `${window.location.origin}/settings/api/notification`;
  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      localStorage.setItem("isActivated", data[0].isActivated);
    });
  // SoundNotification get by id
  let soundNotification = document.getElementById("SoundNotification");
  // console.log(soundNotification);
  // add event listener to soundNotification
  soundNotification.addEventListener("change", (e) => {
    localStorage.setItem("isActivated", e.target.checked);

    // fetch post method to update soundNotification
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ isActivated: e.target.checked }),
    });

    // add to local storage
  });
});
