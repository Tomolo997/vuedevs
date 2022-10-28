$(document).ready(function () {
  // Multiple images preview in browser
  let checkboxes = document.querySelectorAll(".input_role-level");
  $("#new-developer-form").submit(function () {
    var checked = $("input[name='role_level']:checked").length > 0;
    if (!checked) {
      $(".error-role-level-message").show();
      return false;
    } else {
      $(".error-role-level-message").hide();
    }
  });
  let checkboxes_role_type = document.querySelectorAll(".input_role-type");
  $("#new-developer-form").submit(function () {
    var checked_role_type = $("input[name='role_type']:checked").length > 0;
    if (!checked_role_type) {
      $(".error-role-type-message").show();
      return false;
    } else {
      $(".error-role-type-message").hide();
    }
  });
});
