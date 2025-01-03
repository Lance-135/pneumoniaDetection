import React, { useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import Login from "./login";
import SignUp from "./signup";
import PneumoniaRoutes from "./index";
import "./style.css";

function App() {
  const [isSignUpActive, setIsSignUpActive] = useState(false);
  const navigate = useNavigate(); // This will work because App is now wrapped by BrowserRouter

  const toggleToSignUp = () => {
    setIsSignUpActive(true);
  };

  const toggleToSignIn = () => {
    setIsSignUpActive(false);
  };

  const handleLoginSuccess = () => {
    navigate("/index"); // Navigate to /index
  };

  const handleSignUpSuccess = () => {
    navigate("/index"); // Navigate to /index
  };

  return (
    <Routes>
      <Route
        path="/"
        element={
          <div className={`container ${isSignUpActive ? "active" : ""}`} id="container">
            <SignUp toggleToSignIn={toggleToSignIn} onSignUpSuccess={handleSignUpSuccess} />
            <Login toggleToSignUp={toggleToSignUp} onLoginSuccess={handleLoginSuccess} />
            <div className="toggle-container">
              <div className="toggle">
                <div className="toggle-panel toggle-left">
                  <h1>Welcome Back!</h1>
                  <p>Enter your personal details to use all of our site features</p>
                  <button className="hidden" onClick={toggleToSignIn}>Sign In</button>
                </div>
                <div className="toggle-panel toggle-right">
                  <h1>Hello, Friend!</h1>
                  <p>Register with your personal details to use all of our site features</p>
                  <button className="hidden" onClick={toggleToSignUp}>Sign Up</button>
                </div>
              </div>
            </div>
          </div>
        }
      />
      <Route path="/index/*" element={<PneumoniaRoutes />} />
    </Routes>
  );
}

export default App;
