import "../style/Addresses.css";
import FormInput from "./FormInput";
import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import StateDropdown from "./StateDropdown";
import { useApi } from "../hooks";

function AddressList({ addressList }) {
  const queryClient = useQueryClient();
  const api = useApi();

  const mutation = useMutation({
    mutationFn: (address_id) => api.del(`/address/delete/${address_id}`),
    onSuccess: () => {
      console.log("Address deleted successfully!");
      queryClient.invalidateQueries(["addresses"]);
    },
  });

  function onClick(address_id) {
    mutation.mutate(address_id);
  }
  return (
    <div className="address-list-container">
      {addressList &&
        addressList.map((address, index) => (
          <div key={index} className="address">
            <div>
              <p>{address.name}</p>
              <p>{address.address}</p>
              <p>{`${address.city}, ${address.state} ${address.zip}`} </p>
            </div>
            <button onClick={() => onClick(address.id)}>
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        ))}
    </div>
  );
}

function AddAddress() {
  const [name, setAddressName] = useState();
  const [address, setAddress] = useState();
  const [city, setCity] = useState();
  const [state, setState] = useState("");
  const [zip, setZip] = useState();

  const api = useApi();

  const queryClient = useQueryClient();

  const newAddress = {
    name,
    address,
    city,
    state,
    zip,
  };

  const mutation = useMutation({
    mutationFn: () => api.post("/address/post", newAddress),
    onSuccess: () => {
      console.log("Address added successfully!");
      queryClient.invalidateQueries(["addresses"]);
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  };

  return (
    <div className="add-address-container">
      <form className="add-address-form" onSubmit={handleSubmit}>
        <FormInput name="Name" type="text" placeholder="e.g. Giant Food Store" setter={setAddressName}></FormInput>
        <FormInput name="Address" type="text" setter={setAddress}></FormInput>
        <div className="city-state-zip">
          <FormInput name="City" type="text" setter={setCity}></FormInput>
          <StateDropdown selectedState={state} setter={setState}></StateDropdown>
          <FormInput name="zip" type="number" setter={setZip}></FormInput>
        </div>
        <button className="add-address-btn" type="submit">
          Add Address
        </button>
      </form>
    </div>
  );
}

function Addresses({ addressList, isOpen, setIsOpen }) {
  if (!isOpen) {
    return null;
  }
  return (
    <div className="addresses-container">
      <div className="popup-header">
        <div className="invisible"></div>
        <h3>My Addresses</h3>
        <button onClick={() => setIsOpen(false)} className="close-button">
          x
        </button>
      </div>
      <div className="popup-content">
        <AddressList addressList={addressList}></AddressList>
        <AddAddress addressList={addressList}></AddAddress>
      </div>
    </div>
  );
}

export default Addresses;
