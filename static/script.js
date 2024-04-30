




// search input

// function getLocation() {
//     var locationValue = document.getElementById("searchBox").value;
//     var range = document.getElementById("rangeinput").value;

//     // Use Bing Maps Geocoding service to get location coordinates from address
//     Microsoft.Maps.loadModule('Microsoft.Maps.Search', function () {
//         var searchManager = new Microsoft.Maps.Search.SearchManager(map);
//         var requestOptions = {
//             where: locationValue,
//             callback: function (result) {
//                 if (result && result.results && result.results.length > 0) {
//                     var location = result.results[0].location;

//                     // Center the map on the location
//                     map.setView({
//                         center: location
//                     });

//                     // Print latitude and longitude
//                     console.log('Latitude:', location.latitude);
//                     console.log('Longitude:', location.longitude);

//                     // Send to Flask to check in the database and return based on locations
//                     // Send to Flask to check in the database and return based on locations
//                     fetch("/getavailability", {
//                         method: "POST",
//                         headers: {
//                             "Content-Type": "application/json"
//                         },
//                         body: JSON.stringify({ "latitude": location.latitude, "longitude": location.longitude, "range": range })
//                     })
//                         .then(response => {
//                             if (!response.ok) {
//                                 throw new Error("Network response was not ok");
//                             }
//                             return response.json();
//                         })
//                         .then(data => {
//                             console.log("Response from Flask route:", data);

//                             // Loop through each room in the response data
//                             data.rooms_in_range.forEach(room => {
//                                 // Create a location from the room's latitude and longitude
//                                 var roomLocation = new Microsoft.Maps.Location(room.latitude, room.longitude);

//                                 // Create a pushpin to mark the room location
//                                 var pin = new Microsoft.Maps.Pushpin(roomLocation, {
//                                     title: room.address,
//                                     subTitle: room.description
//                                 });

//                                 // Create an infobox for the room
//                                 var infobox = new Microsoft.Maps.Infobox(roomLocation, {
//                                     title: room.address,
//                                     description: room.description,
//                                     showPointer: false,
//                                     showCloseButton: false
//                                 });

//                                 // Add event listener to show infobox when pin is clicked
//                                 Microsoft.Maps.Events.addHandler(pin, 'click', function () {
//                                     // Create the modal elements
//                                     var modal = document.createElement('div');
//                                     modal.classList.add('modal');
//                                     modal.id = 'exampleModalCenter';

//                                     modal.innerHTML = `
//                                     <div class="modal-dialog modal-dialog-centered" role="document">
//                                         <div class="modal-content">
//                                             <div class="modal-header">
//                                                 <h5 class="modal-title">Room ID: ${room.id}</h5>
//                                                 <button type="button" class="close" data-dismiss="modal" aria-label="Close">
//                                                     <span aria-hidden="true">&times;</span>
//                                                 </button>
//                                             </div>
//                                             <div class="modal-body">
//                                                 <strong>Address:</strong> ${room.address} <br>
//                                                 <strong>Description:</strong> ${room.description}
//                                             </div>
//                                             <div class="modal-footer">
//                                                 <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
//                                                 <a type="button" href="/room?id=${room.id}" class="btn btn-primary see">See Details</a>
//                                             </div>
//                                         </div>
//                                     </div>
//                                 `;



//                                     // Append the modal to the document body
//                                     document.body.appendChild(modal);

//                                     // Trigger the modal to show
//                                     $(modal).modal('show');
//                                  // Get the element with class "see"
//                                 // var seeButton = document.querySelector(".see");

//                                 // // Add event listener to the "see" button
//                                 // seeButton.addEventListener('click', function() {
//                                 //     window.location.href = '/room?id=' + room.id;
//                                 // });
//                                 //     // Show the infobox
//                                 //     infobox.setOptions({ visible: true });
//                                 });


//                                 // Add the pin to the map
//                                 map.entities.push(pin);
//                             });
//                         })
//                         .catch(error => {
//                             console.error("Error:", error);
//                         });

//                 } else {
//                     console.error('No results found for the address:', locationValue);
//                 }
//             },
//             errorCallback: function (e) {
//                 console.error('Error:', e);
//             }
//         };

//         searchManager.geocode(requestOptions);
//     });
// }

// second code with red
// function getLocation() {
//     var locationValue = document.getElementById("searchBox").value;
//     var range = document.getElementById("rangeinput").value;

//     // Use Bing Maps Geocoding service to get location coordinates from address
//     Microsoft.Maps.loadModule('Microsoft.Maps.Search', function () {
//         var searchManager = new Microsoft.Maps.Search.SearchManager(map);
//         var requestOptions = {
//             where: locationValue,
//             callback: function (result) {
//                 if (result && result.results && result.results.length > 0) {
//                     var location = result.results[0].location;

//                     // Center the map on the location
//                     map.setView({
//                         center: location
//                     });

//                     // Print latitude and longitude
//                     console.log('Latitude:', location.latitude);
//                     console.log('Longitude:', location.longitude);

//                     // Send to Flask to check in the database and return based on locations
//                     fetch("/getavailability", {
//                         method: "POST",
//                         headers: {
//                             "Content-Type": "application/json"
//                         },
//                         body: JSON.stringify({ "latitude": location.latitude, "longitude": location.longitude, "range": range })
//                     })
//                         .then(response => {
//                             if (!response.ok) {
//                                 throw new Error("Network response was not ok");
//                             }
//                             return response.json();
//                         })
//                         .then(data => {
//                             console.log("Response from Flask route:", data);

//                             // Loop through each room in the response data
//                             data.rooms_in_range.forEach(room => {
//                                 // Create a location from the room's latitude and longitude
//                                 var roomLocation = new Microsoft.Maps.Location(room.latitude, room.longitude);

//                                 // Create a custom red pushpin to mark the room location
//                                 var pin = new Microsoft.Maps.Pushpin(roomLocation, {
//                                     title: room.address,
//                                     subTitle: room.description,
//                                     color: 'red' // Custom red color
//                                 });

//                                 // Add event listener to show infobox when pin is clicked
//                                 Microsoft.Maps.Events.addHandler(pin, 'click', function () {
//                                     // Create the modal elements
//                                     var modal = document.createElement('div');
//                                     modal.classList.add('modal');
//                                     modal.id = 'exampleModalCenter';

//                                     modal.innerHTML = `
//                                     <div class="modal-dialog modal-dialog-centered" role="document">
//                                         <div class="modal-content">
//                                             <div class="modal-header">
//                                                 <h5 class="modal-title">Room ID: ${room.id}</h5>
//                                                 <button type="button" class="close" data-dismiss="modal" aria-label="Close">
//                                                     <span aria-hidden="true">&times;</span>
//                                                 </button>
//                                             </div>
//                                             <div class="modal-body">
//                                                 <strong>Address:</strong> ${room.address} <br>
//                                                 <strong>Description:</strong> ${room.description}
//                                             </div>
//                                             <div class="modal-footer">
//                                                 <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
//                                                 <a type="button" href="/room?id=${room.id}" class="btn btn-primary see">See Details</a>
//                                             </div>
//                                         </div>
//                                     </div>
//                                 `;

//                                     // Append the modal to the document body
//                                     document.body.appendChild(modal);

//                                     // Trigger the modal to show
//                                     var modalElement = document.getElementById('exampleModalCenter');
//                                     var modal = new bootstrap.Modal(modalElement);
//                                     modal.show();
//                                 });

//                                 // Add the pin to the map
//                                 map.entities.push(pin);
//                             });
//                         })
//                         .catch(error => {
//                             console.error("Error:", error);
//                         });

//                 } else {
//                     console.error('No results found for the address:', locationValue);
//                 }
//             },
//             errorCallback: function (e) {
//                 console.error('Error:', e);
//             }
//         };

//         searchManager.geocode(requestOptions);
//     });
// }


// getLocation();

// autosuggest
// Define your Bing Maps API key
// const apiKey = 'AuR5WeOCf_8fh8WSHkMOwevuW0Vnt1MJu0wk-UvPlB7uTdVKErJCCGrzQo0J759C';

// correct code
// var map;

// function GetMap() {
//     map = new Microsoft.Maps.Map('#map', {
//         zoom: 18
//     });
//     // Clear any existing entities on the map
//     map.entities.clear();


//     Microsoft.Maps.loadModule('Microsoft.Maps.AutoSuggest', function () {
//         var manager = new Microsoft.Maps.AutosuggestManager({ map: map });
//         manager.attachAutosuggest('#searchBox', '#searchBoxContainer', suggestionSelected);
//     });
// }







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
    let bingKey = "AuR5WeOCf_8fh8WSHkMOwevuW0Vnt1MJu0wk-UvPlB7uTdVKErJCCGrzQo0J759C";
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

// Function to animate map to the bounds of all pushpins and set zoom level to 18
function animateMapToPushpins() {
    var boundingBox = Microsoft.Maps.LocationRect.fromLocations(map.entities.getPrimitives().filter(function (primitive) {
        return primitive instanceof Microsoft.Maps.Pushpin;
    }).map(function (pin) {
        return pin.getLocation();
    }));

    // Smoothly animate map to the bounds of the pushpins
    Microsoft.Maps.Events.addHandler(map, 'viewchangestart', function () {
        map.setView({ bounds: boundingBox, animate: true });
    });
}

// Create a custom legend control
function addLegendControl() {
    // Define legend content
    var legendContent = `
        <div id="legendControl" style="background-color: white; padding: 10px; border-radius: 5px; box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.3);">
            <h3 style="margin-top: 0;">Legend</h3>
            <div class="legend-item" style="display: flex; align-items: center;">
                <div class="legend-icon" style="width: 20px; height: 20px; border-radius: 50%; background-color: red;"></div>
                <span style="margin-left: 5px;">Available Rooms</span>
            </div>
            <div class="legend-item" style="display: flex; align-items: center; margin-top: 5px;">
                <div class="legend-icon" style="width: 20px; height: 20px; border-radius: 50%; background-color: green;"></div>
                <span style="margin-left: 5px;">Available Roommates</span>
            </div>
        </div>
    `;

    // Create a div element to hold the legend content
    var legendDiv = document.createElement('div');
    legendDiv.innerHTML = legendContent;

    // Add legend control to map
    var legendControl = new Microsoft.Maps.CustomOverlay({
        htmlContent: legendDiv,
        position: map.getTopLeft()
    });

    map.layers.insert(legendControl);
}





function getLocation() {
    var locationValue = document.getElementById("searchBox").value;
    var range = document.getElementById("rangeinput").value;
    map.entities.clear();
    // Use Bing Maps Geocoding service to get location coordinates from address
    Microsoft.Maps.loadModule('Microsoft.Maps.Search', function () {
        var searchManager = new Microsoft.Maps.Search.SearchManager(map);
        var requestOptions = {
            where: locationValue,
            callback: function (result) {
                if (result && result.results && result.results.length > 0) {
                    var searchlocation = result.results[0].location;

                    // Center the map on the location
                    map.setView({
                        center: searchlocation
                    });

                    // Print latitude and longitude
                    console.log('Latitude:', searchlocation.latitude);
                    console.log('Longitude:', searchlocation.longitude);

                    // Send to Flask to check in the database and return based on locations
                    fetch("/getavailability", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ "latitude": searchlocation.latitude, "longitude": searchlocation.longitude, "range": range })
                    })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error("Network response was not ok");
                            }
                            return response.json();
                        })
                        .then(data => {
                            console.log("Response from Flask route:", searchlocation);
                            var pin = new Microsoft.Maps.Pushpin(searchlocation, {
                                title: locationValue ,
                                // subTitle: room.description,
                                // color: 'red' // Custom red color
                            });
                            map.entities.push(pin);
                            var roommateLocation,  roomLocation;
                            // Loop through each room in the response data and create room pushpins
                            data.rooms_in_range.forEach(room => {
                                // Create a location from the room's latitude and longitude
                                roomLocation = new Microsoft.Maps.Location(room.latitude, room.longitude);

                                // Create a custom red pushpin to mark the room location
                                var pin = new Microsoft.Maps.Pushpin(roomLocation, {
                                    title: room.address,
                                    subTitle: room.description,
                                    color: 'red' // Custom red color
                                });

                                // Add event listener to show infobox when room pin is clicked
                                Microsoft.Maps.Events.addHandler(pin, 'click', function () {

                                    // Remove any existing modals
                                    $('.modal').remove();


                                    var modal = document.createElement('div');
                                    modal.classList.add('modal', 'fade'); // Add fade class for smooth animation
                                    modal.id = 'exampleModalCenter';

                                    modal.innerHTML = `
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header" style="background-color: #d84b41; color: white;">
                <h5 class="modal-title">Room ID: ${room.id}</h5>
                <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="row">
                    <div class="col">
                        <p><strong>Address:</strong> ${room.address}</p>
                        <p><strong>Description:</strong> ${room.description}</p>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                <a href="/room?id=${room.id}" class="btn btn-primary">See Details</a>
            </div>
        </div>
    </div>
`;

                                    // Append the modal to the document body
                                    document.body.appendChild(modal);

                                    // Initialize the Bootstrap modal
                                    var modalElement = document.getElementById('exampleModalCenter');
                                    var modalInstance = new bootstrap.Modal(modalElement);
                                    modalInstance.show();
                                });

                                // Add the room pin to the map
                                map.entities.push(pin);
                            });


                            // Loop through each roommate in the response data and create roommate pushpins
                            data.roommates_data.forEach(roommate => {
                                // Create a location from the roommate's latitude and longitude
                                roommateLocation = new Microsoft.Maps.Location(roommate.latitude, roommate.longitude);

                                // Create a custom green pushpin to mark the roommate location
                                var pin = new Microsoft.Maps.Pushpin(roommateLocation, {
                                    title: roommate.address,
                                    subTitle: roommate.gender,
                                    color: 'green' // Custom green color
                                });

                                // Add event listener to show infobox when roommate pin is clicked
                                Microsoft.Maps.Events.addHandler(pin, 'click', function () {
                                    // Create a unique modal for the clicked roommate
                                    // Remove any existing modals
                                    $('.modal').remove();

                                    // Create a unique modal for the clicked room
                                    var modal = document.createElement('div');
                                    modal.classList.add('modal');
                                    modal.id = 'exampleModalCenter';

                                    modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header"style="background-color: #66993a; color: white;">
                        <h5 class="modal-title">Roommate ID: ${roommate.id}</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <strong>Address:</strong> ${roommate.address} <br>
                        <strong>Description:</strong> ${roommate.description} <br> 
                        <strong>Gender:</strong> ${roommate.gender} <br> 
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <a type="button" href="/roommate?id=${roommate.id}" class="btn btn-primary see">See Details</a>
                    </div>
                </div>
            </div>
        `;

                                    // Append the modal to the document body
                                    document.body.appendChild(modal);

                                    // Initialize the Bootstrap modal
                                    var modalElement = document.getElementById('exampleModalCenter');
                                    var modalInstance = new bootstrap.Modal(modalElement);
                                    modalInstance.show();
                                });

                                // Add the room pin to the map
                                map.entities.push(pin);
                            });

                            // Animate map to pushpins and set zoom level to 18
                            // animateMapToPushpins();
                            var centerLocation = roommateLocation || roomLocation;

                            map.setView({
                                center: centerLocation,
                                zoom: 14,
                                animate: true
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




