$(document).ready(function () {
  // Multiple images preview in browser
  $(".button-user-navbar").click(function () {
    $(".navbar__list-display-none").toggleClass("navbar__list");
  });

  $("body").click(function (e) {
    //need to add click outside of the navbar list to clsoe it
  });
});
