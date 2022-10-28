$(document).ready(function () {
  // Multiple images preview in browser
  let arrayOfChecks = window.location.href.split("&");
  let finalArray = [];
  for (let param = 0; param < arrayOfChecks.length; param++) {
    const element = arrayOfChecks[param].split("=")[1];
    finalArray.push(element);
  }

  if (finalArray.includes("junior")) {
    $("#junior").prop("checked", true);
  }
  if (finalArray.includes("senior")) {
    $("#senior").prop("checked", true);
  }
  if (finalArray.includes("mid")) {
    $("#middle").prop("checked", true);
  }
  if (finalArray.includes("principal")) {
    $("#principal").prop("checked", true);
  }
  if (finalArray.includes("part_time_contract")) {
    $("#part_time_contract").prop("checked", true);
  }
  if (finalArray.includes("full_time_job")) {
    $("#full_time_job").prop("checked", true);
  }
  if (finalArray.includes("part_time_job")) {
    $("#part_time_job").prop("checked", true);
  }
  if (finalArray.includes("-12")) {
    $("#GMT-12").prop("checked", true);
  }
  if (finalArray.includes("-11")) {
    $("#GMT-11").prop("checked", true);
  }
  if (finalArray.includes("-10")) {
    $("#GMT-10").prop("checked", true);
  }
  if (finalArray.includes("-09")) {
    $("#GMT-9").prop("checked", true);
  }
  if (finalArray.includes("-08")) {
    $("#GMT-8").prop("checked", true);
  }
  if (finalArray.includes("-07")) {
    $("#GMT-7").prop("checked", true);
  }
  if (finalArray.includes("-06")) {
    $("#GMT-6").prop("checked", true);
  }
  if (finalArray.includes("-05")) {
    $("#GMT-5").prop("checked", true);
  }
  if (finalArray.includes("-04")) {
    $("#GMT-4").prop("checked", true);
  }
  if (finalArray.includes("-03")) {
    $("#GMT-3").prop("checked", true);
  }
  if (finalArray.includes("-02")) {
    $("#GMT-2").prop("checked", true);
  }
  if (finalArray.includes("-01")) {
    $("#GMT-1").prop("checked", true);
  }
  if (finalArray.includes("0")) {
    $("#GMT").prop("checked", true);
  }
  if (finalArray.includes("1")) {
    $("#GMT1").prop("checked", true);
  }
  if (finalArray.includes("2")) {
    $("#GMT2").prop("checked", true);
  }
  if (finalArray.includes("3")) {
    $("#GMT3").prop("checked", true);
  }
  if (finalArray.includes("4")) {
    $("#GMT4").prop("checked", true);
  }
  if (finalArray.includes("5")) {
    $("#GMT5").prop("checked", true);
  }
  if (finalArray.includes("6")) {
    $("#GMT6").prop("checked", true);
  }
  if (finalArray.includes("7")) {
    $("#GMT7").prop("checked", true);
  }
  if (finalArray.includes("8")) {
    $("#GMT8").prop("checked", true);
  }
  if (finalArray.includes("9")) {
    $("#GMT9").prop("checked", true);
  }
  if (finalArray.includes("10")) {
    $("#GMT10").prop("checked", true);
  }
  if (finalArray.includes("11")) {
    $("#GMT11").prop("checked", true);
  }
  if (finalArray.includes("12")) {
    $("#GMT12").prop("checked", true);
  }

  $(".button-filter-clear").click(function (e) {
    e.preventDefault();
    $(".developers-page__filter-input").each(function (i, obj) {
      obj.checked = false;
    });
  });

  $(".legend-seniority").click(function () {
    $(".seniority-dropdown").toggle(".seniority-height");
    if ($(".seniority-chevron").hasClass("seniority-chevron-down")) {
      $(".seniority-chevron")
        .removeClass("seniority-chevron-down")
        .addClass("seniority-chevron-up");
    } else {
      $(".seniority-chevron")
        .removeClass("seniority-chevron-up")
        .addClass("seniority-chevron-down");
    }
  });
  $(".legend-work").click(function () {
    $(".work-dropdown").toggle(".work-height");
    if ($(".work-chevron").hasClass("work-chevron-down")) {
      $(".work-chevron")
        .removeClass("work-chevron-down")
        .addClass("work-chevron-up");
    } else {
      $(".work-chevron")
        .removeClass("work-chevron-up")
        .addClass("work-chevron-down");
    }
  });

  $(".legend-timezone").click(function () {
    $(".timezone-dropdown").toggle(".timezone-height");
    if ($(".timezone-chevron").hasClass("timezone-chevron-down")) {
      $(".timezone-chevron")
        .removeClass("timezone-chevron-down")
        .addClass("timezone-chevron-up");
    } else {
      $(".timezone-chevron")
        .removeClass("timezone-chevron-up")
        .addClass("timezone-chevron-down");
    }
  });
});
