$(document).ready(function () {
  // Multiple images preview in browser
  $(".markdown-div").mouseenter(function () {
    $(".markdown-tooltip").show();
  });
  $(".markdown-div").mouseleave(function () {
    $(".markdown-tooltip").hide();
  });
});
