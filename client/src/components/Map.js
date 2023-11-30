import React, { useState, useEffect } from "react";

const Map = ({ selectedCities, selectedRoutes, dataFromServer }) => {
  const [polylines, setPolylines] = useState([]);

  useEffect(() => {
    // Initialize the map
    const map = new window.google.maps.Map(document.getElementById("map"), {
      center: { lat: 56.1304, lng: -106.3468 },
      zoom: 3.5,
    });

    // Create a dictionary to store info windows for each city
    const infoWindows = {};

    // Add markers for selected cities
    selectedCities.forEach((city) => {
      const geocoder = new window.google.maps.Geocoder();
      geocoder.geocode({ address: city }, (results, status) => {
        if (status === "OK" && results[0].geometry) {
          const marker = new window.google.maps.Marker({
            position: results[0].geometry.location,
            map: map,
            title: city,
          });

          // Create an info window for the marker
          const infoWindow = new window.google.maps.InfoWindow({
            content: `<div>${city}</div>`,
          });

          // Store the info window in the dictionary
          infoWindows[city] = infoWindow;

          // Attach a click event to the marker to open the info window
          marker.addListener("click", () => {
            infoWindow.open(map, marker);
          });
        } else {
          console.error(`Geocoding error for city ${city}: ${status}`);
        }
      });
    });

    // Remove existing polylines
    polylines.forEach((polyline) => {
      polyline.setMap(null);
    });

    // Add polylines for selected routes
    selectedRoutes.forEach((route) => {
      const flightPlanCoordinates = [];

      // Geocode each city in the route to get its coordinates
      route.forEach((city) => {
        const geocoder = new window.google.maps.Geocoder();
        geocoder.geocode({ address: city }, (results, status) => {
          if (status === "OK" && results[0].geometry) {
            flightPlanCoordinates.push(results[0].geometry.location);

            // Draw the polyline when all coordinates are retrieved
            if (flightPlanCoordinates.length === route.length) {
              const flightPath = new window.google.maps.Polyline({
                path: flightPlanCoordinates,
                geodesic: true,
                strokeColor: "#0000FF",
                strokeOpacity: 1.0,
                strokeWeight: 2,
              });
              flightPath.setMap(map);

              // Add the new polyline to the state
              setPolylines((prevPolylines) => [...prevPolylines, flightPath]);
            }
          }
        });
      });
    });

    // Add polylines for selected routes
    const flightPlanCoordinates = dataFromServer.slice(1).map((city) => {
      const geocoder = new window.google.maps.Geocoder();
      return new Promise((resolve, reject) => {
        geocoder.geocode({ address: city }, (results, status) => {
          if (status === "OK" && results[0].geometry) {
            resolve(results[0].geometry.location);
          } else {
            reject(status);
          }
        });
      });
    });

    Promise.all(flightPlanCoordinates)
      .then((locations) => {
        const flightPath = new window.google.maps.Polyline({
          path: locations,
          geodesic: true,
          strokeColor: "#FFFF00",
          strokeOpacity: 1.0,
          strokeWeight: 2,
        });
        flightPath.setMap(map);

        // Add the new polyline to the state
        setPolylines((prevPolylines) => [...prevPolylines, flightPath]);
      })
      .catch((error) => {
        console.error("Geocoding error:", error);
      });

    // Clean up when the component unmounts
    return () => {
      polylines.forEach((polyline) => {
        polyline.setMap(null);
      });
    };
  }, [selectedCities, selectedRoutes, dataFromServer]);

  return <div id="map" style={{ height: "500px", width: "100%" }}></div>;
};

export default Map;
