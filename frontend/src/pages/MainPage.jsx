import "../style/MainPage.css";
import Calculator from "../components/Calculator";
import { useQuery } from "@tanstack/react-query";
import { useAuth, useApi } from "../hooks";

function MainPage() {
  const { logout } = useAuth();
  const api = useApi();

  const { data: addressList } = useQuery({
    queryKey: ["addresses"],
    queryFn: () => api.get("/address/get/all").then((response) => response.json()),
  });

  const onClick = (e) => {
    e.preventDefault();
    logout();
  };

  return (
    <div className="main-page-container">
      <div className="main-page-content">
        <Calculator addressList={addressList}></Calculator>
        <div className="sign-out-container">
          <button className="sign-out-btn" onClick={onClick}>
            Sign Out
          </button>
        </div>
      </div>
    </div>
  );
}

export default MainPage;
