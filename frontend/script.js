$(document).ready(function () {
  var map = L.map("map").setView([40.505, -0.09], 12);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  function getDistance(lat1, lon1, lat2, lon2) {
    var R = 6371; // Radius of the Earth in KM
    var dLat = ((lat2 - lat1) * Math.PI) / 180;
    var dLon = ((lon2 - lon1) * Math.PI) / 180;
    var a =
      0.5 -
      Math.cos(dLat) / 2 +
      (Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        (1 - Math.cos(dLon))) /
        2;
    return R * 2 * Math.asin(Math.sqrt(a));
  }

  function fetchOutlets() {
    $.ajax({
      url: "http://127.0.0.1:8000/outlets/",
      method: "GET",
      success: function (data) {
        data.forEach(function (outlet) {
          var circle = L.circle([outlet.latitude, outlet.longitude], {
            color: "blue",
            fillColor: "#30f",
            fillOpacity: 0.2,
            radius: 50,
          }).addTo(map);

          var marker = L.marker([outlet.latitude, outlet.longitude]).addTo(map);
          marker
            .bindPopup(
              `<ul>
              <li>
                <b>Outlet Name:</b> ${outlet.name}
              </li>
              <li>
                <b>Operating hours: ${outlet.operating_hours}</b>
              </li>
              <li>
                <b>Address:</b> ${outlet.address}
              </li>
              
                </ul>
              
              `
            )
            .openPopup();
        });

        data.forEach(function (outlet1) {
          data.forEach(function (outlet2) {
            if (outlet1.id !== outlet2.id) {
              var distance = getDistance(
                outlet1.latitude,
                outlet1.longitude,
                outlet2.latitude,
                outlet2.longitude
              );
              if (distance < 10) {
                // 10KM because each outlet has 5KM radius
                L.circle([outlet1.latitude, outlet1.longitude], {
                  color: "#0074c6",
                  fillColor: "#0074c6",
                  fillOpacity: 0.02,
                  radius: 500,
                }).addTo(map);
              }
            }
          });
        });
      },
      error: function (error) {
        console.error("Error fetching outlets:", error);
      },
    });
  }

  function searchOutletName(name) {
    var fullName = name.trim().toLowerCase().startsWith("subway")
      ? name
      : `Subway ${name}`;
    $.ajax({
      url: `http://127.0.0.1:8000/outlets/search/?name=${encodeURIComponent(
        fullName
      )}`,
      method: "GET",
      success: function (outlet) {
        var circle = L.circle([outlet.latitude, outlet.longitude], {
          color: "blue",
          fillColor: "#30f",
          fillOpacity: 0.2,
          radius: 50,
        }).addTo(map);

        var marker = L.marker([outlet.latitude, outlet.longitude]).addTo(map);

        marker
          .bindPopup(
            `<ul>
              <li>
                <b>Outlet Name:</b> ${outlet.name}
              </li>
              <li>
                <b>Operating hours: ${outlet.operating_hours}</b>
              </li>
              <li>
                <b>Address:</b> ${outlet.address}
              </li>
              
                </ul>
              
              `
          )
          .openPopup();

        map.setView([outlet.latitude, outlet.longitude], 14);
      },
      error: function (error) {
        console.error("Error fetching outlet: ", error);
        alert("Outlet not found");
      },
    });
  }

  function getDistance(lat1, lon1, lat2, lon2) {
    var R = 6371; // Radius of the Earth in KM
    var dLat = ((lat2 - lat1) * Math.PI) / 180;
    var dLon = ((lon2 - lon1) * Math.PI) / 180;
    var a =
      0.5 -
      Math.cos(dLat) / 2 +
      (Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        (1 - Math.cos(dLon))) /
        2;
    return R * 2 * Math.asin(Math.sqrt(a));
  }

  $("#searchButton").on("click", function () {
    var outletName = $("#outletName").val();
    if (outletName) {
      searchOutletName(outletName);
    }
  });

  fetchOutlets();
});
