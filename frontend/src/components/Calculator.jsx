import "../style/Calculator.css";
import React, { useEffect, useState } from "react";
import FormInput from "./FormInput";
import { useQuery } from "@tanstack/react-query";
import AddressDropdown from "./AddressDropdown";
import { useApi } from "../hooks";
import Addresses from "./Addresses";

function Error({ message }) {
  if (message === "") {
    return <></>;
  }
  return <div className={`error-message ${message === "" ? "" : "error"}`}>{message}</div>;
}

function Calculator({ addressList }) {
  const [isOpen, setIsOpen] = useState(false);
  const api = useApi();
  const [error, setError] = useState("");
  const [buttonClicked, setButtonClicked] = useState(false); // Track button click

  const [storeAddress, setStoreAddress] = useState("");
  const [prevAddress, setPrevAddress] = useState("");

  const [batchPay, setBatchPay] = useState();
  const [numItems, setNumItems] = useState();

  const [distance, setDistance] = useState(0);
  const [prevDistance, setPrevDistance] = useState(0);

  const [secPerItem, setSecPerItem] = useState();

  const [hourly, setHourly] = useState(0);

  const { data: storeCoordsData, refetch: refetchStoreCoords } = useQuery({
    queryKey: ["storeCoords"],
    queryFn: () => api.get(`/google/coords/${storeAddress}`).then((response) => response.json()),
    enabled: false, // Do not run automatically
  });

  const { data: destCoordsData, refetch: refetchDestCoords } = useQuery({
    queryKey: ["destinationCoords"],
    queryFn: () => api.get(`/address/add/${distance}/${storeCoordsData[0]}/${storeCoordsData[1]}`).then((response) => response.json()),
    enabled: false, // Do not run automatically
  });

  const { data: storeToDestinationTime, refetch: refetchStoreToDestinationTime } = useQuery({
    queryKey: ["driveTime"],
    queryFn: () => api.get(`/google/travel_time/${storeAddress}/${destCoordsData}`).then((response) => response.json()),
    enabled: false, // Do not run automatically
  });

  // Handle form submission
  const onSubmit = (e) => {
    e.preventDefault();
    setButtonClicked(true);
    console.log("CLICKED!");
    if (!storeAddress) {
      setError("Please select an address");
    }

    if (storeAddress !== prevAddress) {
      console.log("Store has changed, refeching store coords (GEOCODE!!)... ");
      refetchStoreCoords();
      refetchDestCoords();
      setPrevAddress(storeAddress);
    }

    if (distance !== prevDistance) {
      refetchDestCoords();
      setPrevDistance(distance);
    }
  };

  useEffect(() => {
    if (storeCoordsData) {
      console.log("new store coords", storeCoordsData);
    }
  }, [storeCoordsData]);

  useEffect(() => {
    if (destCoordsData) {
      console.log("Refeching drive time (MATRIX!!)... ");
      console.log("Store Coords", storeCoordsData);
      console.log("Destination Coords: ", destCoordsData);
      refetchStoreToDestinationTime();
    }
  }, [destCoordsData]);

  useEffect(() => {
    if (buttonClicked && storeToDestinationTime) {
      let shopTime = numItems * secPerItem;
      console.log(
        "numItems:",
        numItems,
        "distance:",
        distance,
        "secPerItem:",
        secPerItem,
        "shopTime:",
        shopTime,
        "driveTime:",
        storeToDestinationTime.seconds
      );

      let totalTime = shopTime + storeToDestinationTime.seconds;
      let hourlyWage = batchPay / (totalTime / 3600);
      console.log("total hours:", totalTime / 3600, "hourly", hourlyWage);

      setHourly(hourlyWage);
      setButtonClicked(false);
    }
  }, [buttonClicked, storeToDestinationTime]);

  return (
    <div className="calculator-container">
      <div className="calculator-content">
        <div className="calculator-header">
          <p>Instascart Wage Calculator</p>
          {/* <p>Calculator</p> */}
        </div>
        <form className="calculator-form" onSubmit={onSubmit}>
          <AddressDropdown
            addressList={addressList}
            selectedAddress={storeAddress}
            setter={setStoreAddress}
            placeholder="My Addresses"
            label="Store"
            type="text"
          ></AddressDropdown>
          <button type="button" className="add-button" onClick={() => setIsOpen(true)}>
            Add Store
          </button>
          <FormInput name="Batch Pay $" setter={setBatchPay} placeholder="$20.50" type="number"></FormInput>
          <FormInput name="Distance (miles)" setter={setDistance} placeholder="2" type="number"></FormInput>
          <div className="horizontal">
            <FormInput name="Number of items" setter={setNumItems} placeholder="5" type="number"></FormInput>
            <FormInput name="Seconds Per Item" setter={setSecPerItem} placeholder="60" type="number"></FormInput>
          </div>
          <button type="submit">Calculate</button>
        </form>
        <Error message={error} />
        <div className="result">
          <h3>${hourly.toFixed(2)}</h3> <p>per hour</p>
        </div>

        <Addresses isOpen={isOpen} setIsOpen={setIsOpen} addressList={addressList}></Addresses>
      </div>
    </div>
  );
}
export default Calculator;
