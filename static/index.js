// Requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 6,
  });
  infoWindow = new google.maps.InfoWindow();
  //console.log(infoWindow)
  const locationButton = document.createElement("button");

  locationButton.textContent = "Start Tracking";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
  locationButton.addEventListener("click", () => {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          //console.log(position)
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            accuracy: position.coords.accuracy
          };

          const userAction = async () => {
            console.log(pos)
            const response = await fetch('http://127.0.0.1:5000/pycalcs', {
              method: 'POST',
              body: JSON.stringify(pos), // string or object
              headers: {
                'Content-Type': 'application/json'
              }
            });
            

          const flaskresponse = await response.json(); //extract JSON from the http response
          console.log(flaskresponse)
          // do something with flaskresponse here, probably jsut save inHabit vboolean value
          // and anything that needs to be incremented, no math happens here
        }


      var userradius = {
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center: pos,
            radius: pos.accuracy
        }
        userAction();
          infoWindow.setPosition(pos);
          infoWindow.setContent("User location found.");
          infoWindow.open(map);
          map.setCenter(pos);
          circle = new google.maps.Circle(userradius)
          setTimeout(function(){
          circle.setMap(null);
          }, 3000);

        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        }

        
        
      );
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }

  });


}

// Gets the users location every time interval
window.onload = function(){

  //console.log(document.getElementsByClassName('custom-map-control-button'))

    var loc_button = document.getElementsByClassName('custom-map-control-button');
    setInterval(function(){
        loc_button[0].click();
    },6000);  // clicking every 10 seconds
};

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}