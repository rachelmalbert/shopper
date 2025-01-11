import { QueryClientProvider, QueryClient } from "@tanstack/react-query";
import "./App.css";
import { AuthProvider } from "./context/AuthContext";
import { UserProvider } from "./context/UserContext";
import { useAuth } from "./hooks";
import { BrowserRouter, Navigate, Routes, Route } from "react-router-dom";

//import pages
import MainPage from "./pages/MainPage";
import SigninPage from "./pages/SignInPage";
import SignUpPage from "./pages/SignUpPage";

const queryClient = new QueryClient();

function Main() {
  const { isLoggedIn } = useAuth();

  if (isLoggedIn) {
    return (
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="" element={<MainPage />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    );
  } else {
    return (
      <Routes>
        {/* If the user is not logged in, redirect them to the signin page */}
        <Route path="/" element={<SigninPage />} />
        <Route path="/signup" element={<SignUpPage />} />

        {/* Redirect all other paths to signin */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    );
  }
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <UserProvider>
            <div className="App">
              <Main></Main>
            </div>
          </UserProvider>
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
