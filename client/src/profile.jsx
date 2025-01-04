import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "./index.css";

const Profile = () => {
    const [email, setEmail] = useState("");
    const [name, setName] = useState("");
    const [gender, setGender] = useState("");
    const [address, setAddress] = useState("");
    const [phone, setPhone] = useState("");
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        const storedEmail = localStorage.getItem("userEmail");
        setEmail(storedEmail);
        axios.get(`http://localhost:3001/profile/${storedEmail}`)
            .then(res => {
                const user = res.data;
                setName(user.name);
                setGender(user.gender);
                setAddress(user.address);
                setPhone(user.phone);
            })
            .catch(err => console.error(err));
    }, []);

    const handleSave = async () => {
        try {
            await axios.put(`http://localhost:3001/profile/${email}`, {
                name, gender, address, phone
            });
            alert("Profile updated successfully!");
            setIsEditing(false);
        } catch (error) {
            console.error("Update failed:", error);
        }
    };

    return (
        <div className="profile-container">
            <h2>User Profile</h2>
            <div className="form-group">
                <label>Email (cannot be edited)</label>
                <input value={email} disabled />
            </div>
            <div className="form-group">
                <label>Name</label>
                <input 
                    value={name} 
                    onChange={(e) => setName(e.target.value)} 
                    disabled={!isEditing}
                />
            </div>
            <div className="form-group">
                <label>Gender</label>
                <select 
                    value={gender} 
                    onChange={(e) => setGender(e.target.value)}
                    disabled={!isEditing}
                >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                </select>
            </div>
            <div className="form-group">
                <label>Address</label>
                <input 
                    value={address} 
                    onChange={(e) => setAddress(e.target.value)}
                    disabled={!isEditing}
                />
            </div>
            <div className="form-group">
                <label>Phone</label>
                <input 
                    value={phone} 
                    onChange={(e) => setPhone(e.target.value)}
                    disabled={!isEditing}
                />
            </div>
            {isEditing ? (
                <button onClick={handleSave}>Save Changes</button>
            ) : (
                <button onClick={() => setIsEditing(true)}>Edit Profile</button>
            )}
            <Link to="/index" className="back-button">Back to Home</Link>
        </div>
    );
};

export default Profile;
