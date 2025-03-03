import { createContext, useContext, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { useApi, useAuth } from "../hooks";

const UserContext = createContext();

function UserProvider({ children }) {
  const { isLoggedIn, logout, token } = useAuth();
  const navigate = useNavigate();
  const api = useApi();

  const { data } = useQuery({
    queryKey: ["users", token],
    enabled: isLoggedIn,
    staleTime: Infinity,
    queryFn: () =>
      api.get("/user/self").then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          logout();
          navigate("/");
        }
      }),
  });

  return (
    <UserContext.Provider value={data?.user}>{children}</UserContext.Provider>
  );
}

export { UserContext, UserProvider };
