import React, { useState } from "react";
import Login from "./login";
import SignUp from "./signup";
import Index from "../../index"; 
import { BrowserRouter, Routes, Route, Link } from "react-router-dom"; 
import "./style.css";

function App() {
  const [isSignUpActive, setIsSignUpActive] = useState(false);

  const toggleToSignUp = () => {
    setIsSignUpActive(true);
  };

  const toggleToSignIn = () => {
    setIsSignUpActive(false);
  };

  return (
    <BrowserRouter>
      <Routes>
        {/* Route for Index (Home page after sign-in/signup) */}
        <Route path="/index" element={<Index />} />
        
        {/* Default Route (Home page with SignUp/SignIn) */}
        <Route
          path="/"
          element={
            <div className={`container ${isSignUpActive ? "active" : ""}`} id="container">
              <SignUp toggleToSignIn={toggleToSignIn} />
              <Login toggleToSignUp={toggleToSignUp} />
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
      </Routes>
    </BrowserRouter>
  );
}

export default App;
