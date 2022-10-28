let alertWrapper = document.querySelector(".alert");
let alertClose = document.querySelector(".alert__close");

if (alertWrapper) {
  alertClose.addEventListener("click", () => {
    alertWrapper.style.display = "none";
  });
}

let fieldSetTimezone = document.querySelector(".field-set-timezone");
let fieldsetTimezoneToggleButton = document.querySelector(
  ".field-set-timezone-toggle"
);
let signMinusToggle = document.querySelector(".legend-timezone__minus");
let signPlusToggle = document.querySelector(".legend-timezone__plus");
let legendTimezone = document.querySelector(".legend-timezone");
if (fieldSetTimezone) {
  legendTimezone.addEventListener("click", (e) => {
    fieldSetTimezone.classList.toggle("timezone-height");
  });
}
