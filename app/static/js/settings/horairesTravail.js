// dom content event listener
document.addEventListener("DOMContentLoaded", function () {
  let url = `${window.location.origin}/dashboard/settings/api/WorkHours`;
//   let url = `${window.location.origin}/settings/api/WorkHours`;
  // get workHours element by id
  let workHours = document.getElementById("workHours");
  // get workHoursForm element by id
  let workHoursForm = document.getElementById("workHoursForm");

  let addingTargetWorkHours = document.getElementById("addingTargetWorkHours");

  workHours.addEventListener("click", function (e) {
    let html = addDivForWorkHours();
    //   create div element
    let div = document.createElement("div");

    // add form-control class to div element
    div.className += "form-control relative w-fit mt-2";

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
    addingTargetWorkHours.appendChild(div);
  });

  // get workHoursFormInputsArrayValues element by id
  workHoursForm.addEventListener("submit", function (e) {
    // get workHoursFormInputs element by id
    let workHoursFormInputs = workHoursForm.querySelectorAll("input");
    // get workHoursFormInputsArray element by id
    let workHoursFormInputsArray = Array.from(workHoursFormInputs);

    e.preventDefault();
    // get workHoursFormInputsArrayValues element by id
    let workHoursFormInputsArrayValues = workHoursFormInputsArray.map(
      (input) => {
        return {
          id: input.getAttribute("attr-id"),
          val: input.value,
        };
      }
    );
    // get workHoursFormInputsArrayValues element by id
    workHours.value = workHoursFormInputsArrayValues;
    // crate a new object with first as key and the two next values as value and so on
    const formData = workHoursFormInputsArrayValues
      .map((input, index) => {
        let id = input.id;
        let val = input.val;
        if (index % 3 === 0) {
          let key = input;
          if (key === "" || key === undefined) return undefined;
          let value = workHoursFormInputsArrayValues[index + 1];
          let value2 = workHoursFormInputsArrayValues[index + 2];
          let obj = {
            id: id,
            day: key.val,
            start: value.val,
            end: value2.val,
          };
          return obj;
        }
      })
      .filter((input) => input !== undefined);

    // get workHoursFormInputsArrayValues element by id
    console.log(formData);
    // get workHoursFormInputsArrayValues element by id
    // check if the form is valid and not empty
    fetchAsyncPost(url, formData);
  });
});
