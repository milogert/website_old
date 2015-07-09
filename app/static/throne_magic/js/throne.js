function selectRole() {
  // Indicate the role has been clicked.
  $(this).parent().attr("class", "alert alert-success");

  $(this).attr("class", "selected");

  $("#roles").append("<li>" + $(this).attr("role") + "</li>");

  // Remove the click handler.
  $(this).off("click");

  // Make ajax call to server to get the roles allowed.
  jQuery.ajax({
    type: "POST",
    url: "/throne_magic/api/select",
    data: {
      aRole: $(this).attr("role")
    },
    success: function(theData) {
      // Get a json object back and parse it.
      // var aJson = $.parseJSON(theData);
      var aMustElim = $.parseJSON(theData["mustElim"]);
      var aElimBy = $.parseJSON(theData["elimBy"]);

      // Disable everything.
      $(".available, .disabled").each(function (i) {
        var aEle = $(this);

        var aId = parseInt(aEle.attr("id"));

        if(aMustElim.indexOf(aId) >= 0 && aElimBy.indexOf(aId) >= 0) {
          aEle.attr("class", "available");
          aEle.parent().attr("class", "alert alert-info");

          // Fade back in.
          aEle.fadeTo(0, 1);

          // Reactivate the click handler.
          aEle.off("click");
          aEle.on("click", selectRole);
        } else {
          aEle.attr("class", "disabled");
          aEle.parent().attr("class", "alert alert-danger");

          // Fade it out.
          aEle.fadeTo(0, 0.5);

          // Remove click handler.
          aEle.off("click");
        }
      });
    },
    dataType: "json"
  });
}

function selectRandom() {
  jQuery.ajax({
    type: "GET",
    url: "/throne_magic/api/random",
    data: {
      aNumber: $("#players").val()
    },
    success: function(theData) {
      // Get a json object back and parse it.
      //var aSelected = $.parseJSON(theData);
      var aHtml = "";

      // Generate new html.
      $.each(theData, function(aIndex, aValue) {
        aHtml = aHtml.concat(
          '<div class="col-md-3"><div class="well"><img src="/static/throne_magic/img/roles/' + aValue + '.gif"></div></div>'
        );
      });

      // Insert the new html.
      $("#holder").html(aHtml);
    },
    dataType: "json"
  });

}

$(function () {
  $(".available").on("click", selectRole);

  // $("#submit").on("click", selectRandom);
});