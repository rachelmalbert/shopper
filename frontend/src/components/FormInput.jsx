import "../style/FormInput.css";

function FormInput({ setter, ...props }) {
  let placeholder = props.name;
  if (props.placeholder) {
    placeholder = props.placeholder;
  }
  function handleChange(event) {
    setter(event.target.value.toLowerCase());
  }

  return (
    <div className="input">
      <label htmlFor={props.name}>{props.name}</label>
      <input
        type={props.type}
        name={props.name}
        id={props.name}
        onChange={handleChange}
        placeholder={placeholder}
        required
      ></input>
    </div>
  );
}

export default FormInput;
