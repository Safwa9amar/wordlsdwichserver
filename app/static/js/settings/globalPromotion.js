// add domcontent load event listener
document.addEventListener("DOMContentLoaded", function () {
  // get the element with id 'globalPromotion'
  var globalPromotion = document.getElementById("globalPromotion");
  var globalPromotionTarget = document.getElementById("globalPromotionTarget");

  // add event listener to the element
  globalPromotion.addEventListener("change", function () {
    // get the value of the element
    var value = globalPromotion.value;
    let html = `
            ${
              value > 0
                ? '<span class="text-green-500">' + value + "%</span>"
                : '<span class="text-red-500">0%</span>'
            }
        `;
    globalPromotionTarget.innerHTML = html;

    // push data to the server using fetchAsyncPost function
    // fetchAsyncPost("dashboard/settings/api/globalPromotion", {
    fetchAsyncPost("/settings/api/globalPromotion", {
      globalPromotion: value,
    });
  });
});
