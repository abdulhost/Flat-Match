// search input

function getLocation() {
    var locationValue = document.getElementById("searchBox").value;
    var range = document.getElementById("rangeinput").value;

    // Use Bing Maps Geocoding service to get location coordinates from address
    Microsoft.Maps.loadModule('Microsoft.Maps.Search', function () {
        var searchManager = new Microsoft.Maps.Search.SearchManager(map);
        var requestOptions = {
            where: locationValue,
            callback: function (result) {
                if (result && result.results && result.results.length > 0) {
                    var location = result.results[0].location;

                    // Center the map on the location
                    map.setView({
                        center: location
                    });

                    // Print latitude and longitude
                    console.log('Latitude:', location.latitude);
                    console.log('Longitude:', location.longitude);

                    // Send to Flask to check in the database and return based on locations
                    // Send to Flask to check in the database and return based on locations
                    fetch("/getavailability", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ "latitude": location.latitude, "longitude": location.longitude, "range": range })
                    })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error("Network response was not ok");
                            }
                            return response.json();
                        })
                        .then(data => {
                            console.log("Response from Flask route:", data);

                            // Loop through each room in the response data
                            data.rooms_in_range.forEach(room => {
                                // Create a location from the room's latitude and longitude
                                var roomLocation = new Microsoft.Maps.Location(room.latitude, room.longitude);

                                // Create a pushpin to mark the room location
                                var pin = new Microsoft.Maps.Pushpin(roomLocation, {
                                    title: room.address,
                                    subTitle: room.description
                                });

                                // Create an infobox for the room
                                var infobox = new Microsoft.Maps.Infobox(roomLocation, {
                                    title: room.address,
                                    description: room.description,
                                    showPointer: false,
                                    showCloseButton: false
                                });

                                // Add event listener to show infobox when pin is clicked
                                Microsoft.Maps.Events.addHandler(pin, 'click', function () {
                                    // Create the modal elements
                                    var modal = document.createElement('div');
                                    modal.classList.add('modal');
                                    modal.id = 'exampleModalCenter';
                                
                                    modal.innerHTML = `
                                    <div class="modal-dialog modal-dialog-centered" role="document">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title">Room ID: ${room.id}</h5>
                                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                    <span aria-hidden="true">&times;</span>
                                                </button>
                                            </div>
                                            <div class="modal-body">
                                                <strong>Address:</strong> ${room.address} <br>
                                                <strong>Description:</strong> ${room.description}
                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                                <a type="button" href="/room?id=${room.id}" class="btn btn-primary see">See Details</a>
                                            </div>
                                        </div>
                                    </div>
                                `;
                                
                               
                                
                                    // Append the modal to the document body
                                    document.body.appendChild(modal);
                                
                                    // Trigger the modal to show
                                    $(modal).modal('show');
                                 // Get the element with class "see"
                                // var seeButton = document.querySelector(".see");
                                
                                // // Add event listener to the "see" button
                                // seeButton.addEventListener('click', function() {
                                //     window.location.href = '/room?id=' + room.id;
                                // });
                                //     // Show the infobox
                                //     infobox.setOptions({ visible: true });
                                });
                                

                                // Add the pin to the map
                                map.entities.push(pin);
                            });
                        })
                        .catch(error => {
                            console.error("Error:", error);
                        });

                } else {
                    console.error('No results found for the address:', locationValue);
                }
            },
            errorCallback: function (e) {
                console.error('Error:', e);
            }
        };

        searchManager.geocode(requestOptions);
    });
}


// getLocation();

// autosuggest
// Define your Bing Maps API key
// const apiKey = 'AuR5WeOCf_8fh8WSHkMOwevuW0Vnt1MJu0wk-UvPlB7uTdVKErJCCGrzQo0J759C';

var map;

function GetMap() {
    map = new Microsoft.Maps.Map('#map', {
        zoom: 18
    });
    // Clear any existing entities on the map
    map.entities.clear();


    Microsoft.Maps.loadModule('Microsoft.Maps.AutoSuggest', function () {
        var manager = new Microsoft.Maps.AutosuggestManager({ map: map });
        manager.attachAutosuggest('#searchBox', '#searchBoxContainer', suggestionSelected);
    });
}

function suggestionSelected(result) {
    //Remove previously selected suggestions from the map.
    map.entities.clear();

    //Show the suggestion as a pushpin and center map over it.
    var pin = new Microsoft.Maps.Pushpin(result.location);
    map.entities.push(pin);

    map.setView({ bounds: result.bestView });
}
(async () => {
    let script = document.createElement("script");
    // let bingKey = "AuR5WeOCf_8fh8WSHkMOwevuW0Vnt1MJu0wk-UvPlB7uTdVKErJCCGrzQo0J759C";
    script.setAttribute("src", `https://www.bing.com/api/maps/mapcontrol?callback=GetMap&key=${bingKey}`);
    document.body.appendChild(script);
})();




// marker and displaying map
// var map, infobox;

// function GetMap() {
//     map = new Microsoft.Maps.Map('#map', {
//         zoom: 17
//     });

//     var address = 'Gali number 24, Tugalkabad, New Delhi'; // Address to display

//     // Use Bing Maps Geocoding service to get location coordinates from address
//     Microsoft.Maps.loadModule('Microsoft.Maps.Search', function () {
//         var searchManager = new Microsoft.Maps.Search.SearchManager(map);
//         var requestOptions = {
//             where: address,
//             callback: function (result) {
//                 if (result && result.results && result.results.length > 0) {
//                     var location = result.results[0].location;

//                     // Center the map on the location
//                     map.setView({
//                         center: location
//                     });

//                     // Create a pushpin to mark the location
//                     var pin = new Microsoft.Maps.Pushpin(location, {
//                         title: address,
//                         subTitle: 'Click for more info'
//                     });

//                     // Create an infobox
//                     infobox = new Microsoft.Maps.Infobox(location, {
//                         title: address,
//                         description: 'This is the location available.',
//                         showPointer: false,
//                         showCloseButton: false,
//                         actions: [{
//                             label: 'More Info',
//                             eventHandler: function () {
//                                 alert('More information can be displayed here.');
//                             }
//                         }]
//                     });

//                     // Add event listener to show infobox when pin is clicked
//                     Microsoft.Maps.Events.addHandler(pin, 'click', function () {
//                         infobox.setOptions({ visible: true });
//                     });

//                     // Add the pin and infobox to the map
//                     map.entities.push(pin);
//                     map.entities.push(infobox);

//                     // Print latitude and longitude
//                     console.log('Latitude:', location.latitude);
//                     console.log('Longitude:', location.longitude);
//                 } else {
//                     console.error('No results found for the address:', address);
//                 }
//             },
//             errorCallback: function (e) {
//                 console.error('Error:', e);
//             }
//         };

//         searchManager.geocode(requestOptions);
//     });
// }
//  // Dynamic load the Bing Maps Key and Script
//  (async () => {
//     let script = document.createElement("script");
//     // let bingKey = "AuR5WeOCf_8fh8WSHkMOwevuW0Vnt1MJu0wk-UvPlB7uTdVKErJCCGrzQo0J759C"; // Your Bing Maps API key
//     script.setAttribute("src", `https://www.bing.com/api/maps/mapcontrol?callback=GetMap&key=${bingKey}`);
//     document.body.appendChild(script);
// })();


