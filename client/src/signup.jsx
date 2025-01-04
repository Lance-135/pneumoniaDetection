import axios from 'axios';
import { useState } from "react";
import "./style.css";
import { useNavigate } from "react-router-dom";

function SignUp() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!name || !email || !password) {
            alert("Please fill out all fields.");
            return;
        }

        try {
            const response = await axios.post('http://localhost:3001/signup', { name, email, password });
            if (response.data.error) {
                alert(response.data.error);
            } else {
                alert("Signup successful!");
                localStorage.setItem("userEmail", email);
                localStorage.setItem("userName", name);
                navigate('/index');
            }
        } catch (error) {
            alert("An error occurred. Please try again.");
        }
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
                <input 
                    type="password" 
                    placeholder="Password" 
                    onChange={(e) => setPassword(e.target.value)} 
                    value={password} 
                />
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
}

export default SignUp;
