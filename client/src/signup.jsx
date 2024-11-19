import axios from 'axios';
import { useState } from "react";
import "./style.css";
import { useNavigate } from "react-router-dom";

function SignUp() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false); 
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();

        // Validate all fields
        if (!name || !email || !password) {
            alert("Please fill out all fields.");
            return;
        }

        axios.post('http://localhost:3001/signup', { name, email, password })
            .then((result) => {
                console.log(result);
                
                if (result.data.error) {
                    console.error("Error from server:", result.data.error);
                    alert("Error: " + result.data.error); 
                } else {
                    console.log("User created successfully:", result.data);
                    alert("Signup successful!");
                    navigate('/Index');
                }
            })
            .catch((err) => {
                console.error("Request failed:", err);
                alert("An error occurred. Please try again.");
            });
    };

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword); 
    };

    return (
        <div className="form-container sign-up">
            <form onSubmit={handleSubmit}>
                <h1>Create Account</h1>
                <input 
                    type="text" 
                    placeholder="Name" 
                    onChange={(e) => setName(e.target.value)} 
                    value={name} 
                />
                <input 
                    type="email" 
                    placeholder="Email" 
                    onChange={(e) => setEmail(e.target.value)} 
                    value={email} 
                />
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

                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
}

export default SignUp;
