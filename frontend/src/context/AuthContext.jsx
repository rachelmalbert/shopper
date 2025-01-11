import { createContext, useState, useEffect } from "react";

const getToken = () => sessionStorage.getItem("__shopper_token__");
const storeToken = (token) => sessionStorage.setItem("__shopper_token__", token);
const clearToken = () => sessionStorage.removeItem("__shopper_token__");

const AuthContext = createContext();

function AuthProvider({ children }) {
  const [token, setToken] = useState(getToken);

  useEffect(() => {
    if (token) {
      storeToken(token);
    } else {
      clearToken();
    }
  }, [token]);

  const login = (tokenData) => {
    setToken(tokenData.access_token);
    console.log("logged in and token set");
  };

  const logout = () => {
    setToken(null);
    clearToken();
  };

  const isLoggedIn = !!token;

  const contextValue = {
    login,
    token,
    isLoggedIn,
    logout,
  };

  return <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>;
}

export { AuthContext, AuthProvider };
