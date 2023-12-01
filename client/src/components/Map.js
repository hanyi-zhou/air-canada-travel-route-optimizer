import React, { useState, useEffect } from "react";

const Map = ({ selectedCities, selectedRoutes, dataFromServer }) => {
  const [polylines, setPolylines] = useState([]);

  useEffect(() => {
    const map = new window.google.maps.Map(document.getElementById("map"), {
      center: { lat: 56.1304, lng: -106.3468 },
      zoom: 3.5,
    });

    const infoWindows = {};

    selectedCities.forEach((city) => {
      const geocoder = new window.google.maps.Geocoder();
      geocoder.geocode({ address: city }, (results, status) => {
        if (status === "OK" && results[0].geometry) {
          const marker = new window.google.maps.Marker({
            position: results[0].geometry.location,
            map: map,
            title: city,
          });

          const infoWindow = new window.google.maps.InfoWindow({
            content: `<div>${city}</div>`,
          });

          infoWindows[city] = infoWindow;

          marker.addListener("click", () => {
            infoWindow.open(map, marker);
          });
        } else {
          console.error(`Geocoding error for city ${city}: ${status}`);
        }
      });
    });

    const addPolyline = (coordinates, color) => {
      const flightPath = new window.google.maps.Polyline({
        path: coordinates,
        geodesic: true,
        strokeColor: color,
        strokeOpacity: 1.0,
        strokeWeight: 2,
      });
      flightPath.setMap(map);
      setPolylines((prevPolylines) => [...prevPolylines, flightPath]);
    };

    selectedRoutes.forEach((route) => {
      const flightPlanCoordinates = [];

      route.forEach((city) => {
        const geocoder = new window.google.maps.Geocoder();
        geocoder.geocode({ address: city }, (results, status) => {
          if (status === "OK" && results[0].geometry) {
            flightPlanCoordinates.push(results[0].geometry.location);

            if (flightPlanCoordinates.length === route.length) {
              addPolyline(flightPlanCoordinates, "#0000FF");
            }
          }
        });
      });
    });

    const resultCoordinates = dataFromServer.slice(1).map((city) => {
      return new Promise((resolve, reject) => {
        const geocoder = new window.google.maps.Geocoder();
        geocoder.geocode({ address: city }, (results, status) => {
          if (status === "OK" && results[0].geometry) {
            resolve(results[0].geometry.location);
          } else {
            reject(status);
          }
        });
      });
    });

    Promise.all(resultCoordinates)
      .then((locations) => {
        // Remove existing polylines before adding the result polyline
        polylines.forEach((polyline) => {
          polyline.setMap(null);
        });
        addPolyline(locations, "#FFFF00");
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
    // eslint-disable-next-line
  }, [selectedCities, selectedRoutes, dataFromServer]);

  return <div id="map" style={{ height: "500px", width: "100%" }}></div>;
};

export default Map;
