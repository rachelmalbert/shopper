import { useState } from "react";
import { useNavigate } from "react-router-dom";
import FormInput from "../components/FormInput";
import { useAuth } from "../hooks";
import api from "../api";
import "../style/SignInPage.css";

function Error({ message }) {
  if (message === "") {
    return <></>;
  }
  return <div className="text-red-300 text-xs">{message}</div>;
}

function SignUpLink() {
  return (
    <div className="signup-link">
      <p className="signup-link-text">
        Don't have an account?
        <a href="/signup" className="signup-link-text">
          Sign Up
        </a>
      </p>
    </div>
  );
}

function SigninPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useAuth();
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const onSubmit = (e) => {
    e.preventDefault();

    api()
      .postForm("/auth/token", { username, password })
      .then((response) => {
        if (response.ok) {
          response
            .json()
            .then(login)
            .then(() => navigate("/"));
        } else if (response.status === 401) {
          response.json().then((data) => {
            setError("Username or password incorrect");
          });
        } else {
          setError("error logging in");
        }
      });
  };

  return (
    <div className="login-container">
      <form className="login-form-container" onSubmit={onSubmit}>
        <div className="logo-container">
          <div className="logo-title">Sign In</div>
        </div>

        <FormInput type="text" name="Username" id="username" setter={setUsername} />
        <FormInput type="password" name="Password" id="password" setter={setPassword} />
        {/* Forgot password link */}
        <div className="forgot-password-link">
          <a href="/forgot-password" className="forgot-password-text">
            Forgot Password?
          </a>
        </div>
        <button className="sign-in-button" type="submit">
          Sign In
        </button>
        <Error message={error} />
        <SignUpLink></SignUpLink>
      </form>
    </div>
  );
}

export default SigninPage;
