import axios from 'axios'
import { useState } from "react";
import "./style.css";
import {useNavigate} from "react-router-dom";


function login() {
    
    const [email,setEmail]=useState()
    const [password,setPassword]=useState()
    const [showPassword, setShowPassword] = useState(false); 
    const navigate = useNavigate()

    const handleSubmit = (e) => {
      e.preventDefault();
      axios.post('http://localhost:3001/login', { email, password })
        .then((result) => { 
          console.log(result)
          if(result.data === "Success") {
            alert("Signup successful!");
            navigate('/Index')
          } else {
            alert("Email or password is incorrect")
          }
          
        })
        .catch((err) => {
          console.log("Request failed:", err);
          alert("An error occurred. Please try again.");
        });
    };
    
    const togglePasswordVisibility = () => {
      setShowPassword(!showPassword); 
  };

  return (
    <div className="form-container sign-in">
      <form onSubmit={handleSubmit}> 
        <h1>Sign In</h1>
        <input type="email" placeholder="Email"
                    onChange={(e) => setEmail(e.target.value) }/> 
        <div className="password-container">
                      <input 
                          type={showPassword ? "text" : "password"} 
                          placeholder="Enter your Password" 
                          onChange={(e) => setPassword(e.target.value)} 
                          value={password} 
                      />
                      <img 
                          src={showPassword ? "/hide.png" : "/view.png"} 
                          alt={showPassword ? "Hide Password" : "Show Password"} 
                          className="password-icon" 
                          onClick={togglePasswordVisibility}
                      />
                    </div>
        <a href="#">Forget Your Password?</a>
        
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
};

export default login;