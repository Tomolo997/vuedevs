$(document).ready(function () {
  // Multiple images preview in browser
  let imageDiv = document.querySelector(".create-developer__image-img");
  let imgInp = document.getElementById("id_profile_image");
  $("#id_profile_image").on("change", function () {
    const fileSize = this.files[0].size / 1024 / 1024;
    if (fileSize > 2) {
      $(".error-file").removeClass("error-not-visible");
      $(".create-developer__button-real").prop("disabled", true);
    } else {
      $(".error-file").addClass("error-not-visible");
      $(".create-developer__button-real").prop("disabled", false);
    }
  });
  imgInp.onchange = (evt) => {
    const [file] = imgInp.files;
    if (file) {
      imageDiv.src = URL.createObjectURL(file);
    }
  };
});
