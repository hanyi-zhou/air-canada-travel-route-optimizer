import React, { useState, useEffect } from "react";
import Map from "./components/Map";
import "./App.css";

const App = () => {
  const predefinedCities = [
    "Vancouver-BC",
    "PrinceGeorge-BC",
    "Yellowknife-NT",
    "Calgary-AB",
    "Edmonton-AB",
    "Saskatoon-SK",
    "Regina-SK",
    "Winnipeg-MB",
    "Toronto-ON",
    "Ottawa-ON",
    "Montreal-QC",
    "Quebec-QC",
    "Halifax-NS",
  ];

  const initialData = {
    selectedCities: [],
    selectedCity: "",
    selectedRoutes: [],
    dataFromServer: [],
  };

  const [selectedCities, setSelectedCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState("");
  const [selectedRoutes, setSelectedRoutes] = useState([]);
  const [dataFromServer, setDataFromServer] = useState([]);

  const handleCitySelect = (event) => {
    setSelectedCity(event.target.value);
  };

  const handleAddCity = () => {
    // Find the index of the selected city in predefinedCities
    const indexInPredefinedCities = predefinedCities.indexOf(selectedCity);
    const currentLength = selectedCities.length;

    // Add the selected city to the list at the correct index
    if (
      indexInPredefinedCities !== -1 &&
      !selectedCities.includes(selectedCity)
    ) {
      // Find the correct position to insert the selected city
      let insertIndex = 0;
      while (
        insertIndex < currentLength &&
        indexInPredefinedCities >
          predefinedCities.indexOf(selectedCities[insertIndex])
      ) {
        insertIndex++;
      }

      // Insert the selected city at the correct position
      setSelectedCities((prevCities) => [
        ...prevCities.slice(0, insertIndex),
        selectedCity,
        ...prevCities.slice(insertIndex),
      ]);
    }

    // Clear the selected city
    setSelectedCity("");
  };

  const handleRouteSubmit = (event) => {
    event.preventDefault();

    const fromCity = event.target.elements.from.value;
    const toCity = event.target.elements.to.value;

    // Check if both "from" and "to" cities are selected and different
    if (fromCity && toCity && fromCity !== toCity) {
      const newRoute = [fromCity, toCity];
      setSelectedRoutes([...selectedRoutes, newRoute]);
    } else {
      alert("Please select two different cities!");
    }

    // Clear the input fields
    event.target.elements.from.value = "";
    event.target.elements.to.value = "";
  };

  const handleRouteCitySelect = (index, event) => {
    const updatedRoutes = selectedRoutes.map((route, i) => {
      if (i === index) {
        return [event.target.value, route[1]];
      }
      return route;
    });
    setSelectedRoutes(updatedRoutes);
  };

  useEffect(() => {
    // Additional side effects or data fetching can be handled here
  }, [selectedCities, selectedRoutes]);

  const handleSubmit = async () => {
    try {
      const response = await fetch(
        `https://final-project-406621.uw.r.appspot.com/api/process_data`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            selectedCities: selectedCities,
            selectedRoutes: selectedRoutes,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      const serverResult = result.result;
      setDataFromServer(serverResult);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleReset = () => {
    // Reset all state variables to their initial values
    setSelectedCities(initialData.selectedCities);
    setSelectedCity(initialData.selectedCity);
    setSelectedRoutes(initialData.selectedRoutes);
    setDataFromServer(initialData.dataFromServer);
  };

  return (
    <div>
      <h1 className="title">Air Canada Travel Route Optimizer</h1>
      <div className="addMenu">
        <label className="selectCity">
          Select City:
          <select
            className="selectCityMenu"
            onChange={handleCitySelect}
            value={selectedCity}
          >
            <option value="" disabled>
              Select a city
            </option>
            {predefinedCities.map((city, index) => (
              <option key={index} value={city}>
                {city}
              </option>
            ))}
          </select>
        </label>
        <button className="addCityButton" onClick={handleAddCity}>
          Add City
        </button>
        <br />
        <br />
        <form onSubmit={handleRouteSubmit}>
          <label className="from">
            From:
            <select
              className="selectRouteMenuFrom"
              name="from"
              onChange={(e) => handleRouteCitySelect(selectedRoutes.length, e)}
            >
              <option value="" disabled>
                Select a city
              </option>
              {selectedCities.map((city, index) => (
                <option key={index} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </label>
          <label className="to">
            To:
            <select
              className="selectRouteMenuTo"
              name="to"
              onChange={(e) => handleRouteCitySelect(selectedRoutes.length, e)}
            >
              <option value="" disabled>
                Select a city
              </option>
              {selectedCities.map((city, index) => (
                <option key={index} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </label>
          <button className="addRouteButton" type="submit">
            Add Route
          </button>
        </form>
        <br />
        <button className="calculateResultButton" onClick={handleSubmit}>
          Calculate Result
        </button>
        <button className="resetButton" onClick={handleReset}>
          Reset
        </button>
      </div>
      <hr />
      <div className="cities">
        <h2>Selected Cities:</h2>
        <ul>
          {selectedCities.map((city, index) => (
            <li key={index}>
              {" "}
              {index === 0
                ? "Westernmost: "
                : index === selectedCities.length - 1
                  ? "Easternmost: "
                  : ""}
              {city}
            </li>
          ))}
        </ul>
      </div>
      <hr />
      <div className="routes">
        <h2>Selected Routes:</h2>
        <ul>
          {selectedRoutes.map((route, index) => (
            <li key={index}>{`${route[0]} ⇌ ${route[1]}`}</li>
          ))}
        </ul>
      </div>
      <hr />
      <div className="result">
        <h2>Result:</h2>
        <p className="resultDetails">
          Maximum number of cities in the route: {dataFromServer[0]}
          <br />
          Route: {dataFromServer.slice(1).join(" → ")}
        </p>
      </div>

      <div>
        <Map
          selectedCities={selectedCities}
          selectedRoutes={selectedRoutes}
          dataFromServer={dataFromServer}
        />
      </div>
    </div>
  );
};

export default App;
