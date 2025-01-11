import "../style/AddressDropdown.css";

function AddressDropdown({ selectedAddress, setter, addressList, label }) {
  function handleChange(event) {
    setter(event.target.value);
  }

  return (
    <div className="dropdown input">
      <label>{label}</label>
      <select value={selectedAddress} onChange={handleChange}>
        <option value="" disabled>
          My Addresses
        </option>
        {addressList &&
          addressList.map((address, index) => (
            <option key={index} value={`${address.address}, ${address.city}, ${address.state} ${address.zip}`}>
              {`${address.name} -- ${address.address}, ${address.city}, ${address.state} ${address.zip}`}
            </option>
          ))}
      </select>
    </div>
  );
}

export default AddressDropdown;
