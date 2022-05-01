// Requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 51.078818919, lng: -114.1304226},
    zoom: 17,
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
            
          console.log("here");  
          const flaskresponse = await response.json(); //extract JSON from the http response
          console.log(flaskresponse)

          flaskresponse = flaskresponse.parse();
          
          // test = flaskresponse['building_lat'];
          // console.log(test)

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

  var tfdlcontentString = "Location: TFDL, Habit: Eduction, Status: Not in Range"
  var tfdlinfowindow = new google.maps.InfoWindow({
        content: tfdlcontentString
      });
       
    var tfdladius = {
          strokeColor: '#00FFFF',
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: '#00FFFF',
          fillOpacity: 0.45,
          map: map,
          center: { lat: 51.077271, lng: -114.130058, accuracy: 50},
          radius: 50
      }
    tfdlcircle = new google.maps.Circle(tfdladius)

    tfdlmarker = new google.maps.Marker({
    position: tfdladius.center,
    map: map,
    title: "tfdl marker",
  });

    tfdlmarker.addListener('click', function() {
    tfdlinfowindow.open(map, tfdlmarker);
  });


  var gymcontentString = "Location: UofC Active Living, Habit: Fitness, Status: Not in Range"
  var gyminfowindow = new google.maps.InfoWindow({
        content: gymcontentString
      });
       
    var gymradius = {
          strokeColor: '#9F2B68',
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: '#9F2B68',
          fillOpacity: 0.45,
          map: map,
          center: { lat: 51.076340, lng: -114.131520, accuracy: 50},
          radius: 60
      }
    tfdlcircle = new google.maps.Circle(gymradius)

   gymmarker = new google.maps.Marker({
    position: gymradius.center,
    map: map,
    title: "gym marker",
  });

    gymmarker.addListener('click', function() {
    gyminfowindow.open(map, gymmarker);
  });


   var eelcontentString = "Location: Energy Environment and Experiential Learning Building, Habit: Fitness, Status: In Range"
  var eelinfowindow = new google.maps.InfoWindow({
        content: eelcontentString
      });
       
    var eelradius = {
          strokeColor: '#0000FF',
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: '#0000FF',
          fillOpacity: 0.45,
          map: map,
          center: { lat: 51.08122, lng: -114.1295, accuracy: 50},
          radius: 60
      }
    eelcircle = new google.maps.Circle(eelradius)

   eelmarker = new google.maps.Marker({
    position: eelradius.center,
    map: map,
    title: "eel marker",
  });

    eelmarker.addListener('click', function() {
    eelinfowindow.open(map, eelmarker);
  });
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