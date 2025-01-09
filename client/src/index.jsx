import React, { useState } from "react";
import { Routes, Route, Link, Outlet } from "react-router-dom"; 
import axios from "axios";
import Profile from "./profile";
import History from "./history";
import "./index.css";

const PneumoniaDetection = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewSrc, setPreviewSrc] = useState("");
  const [result, setResult] = useState("");
  const [accuracy, setAccuracy] = useState("");
  const email = localStorage.getItem("userEmail"); // Fetch email for saving data

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreviewSrc(e.target.result);
        setResult("");
        setAccuracy("");
      };
      reader.readAsDataURL(file);
    }
  };

  const handlePrediction = async () => {
    if (!selectedFile) return alert("Please upload an image first!");

    const formData = new FormData();
    formData.append("image", selectedFile);
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    try {
      setResult("Processing...");
      setAccuracy("");
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
        signal: controller.signal,
      });
      clearTimeout(timeoutId);
      const data = await response.json();
      setResult(data.result || "Error processing the image");
      setAccuracy(data.accuracy ? `${(data.accuracy * 100).toFixed(2)}%` : "");

      // ✅ Store the prediction result in MongoDB
      await axios.post(`http://localhost:3001/save-prediction/${email}`, {
        image: previewSrc, 
        result: data.result,
        confidence: data.accuracy
      });
      alert("Prediction result saved to your history.");
    } catch (error) {
      // setResult(error.message);
    }
  };

  return (
    <div id="ccontainer">
      <header>
        Pneumonia Detection
        <div className="header-buttons">
          <Link to="profile" className="header-button">
            <img src="./profile.png" alt="Profile" width="24" height="24" />
          </Link>
          <Link to="history" className="header-button">
            <img src="./history.png" alt="History" width="24" height="24" />
          </Link>
        </div>
      </header>
      <Outlet />
      <div id="content">
        <div id="left-panel">
          <input
            type="file"
            id="file-input"
            accept="image/*"
            onChange={handleFileChange}
          />
          {selectedFile && (
            <button id="predict-btn" onClick={handlePrediction}>
              Predict
            </button>
          )}
        </div>
        <div id="rright-panel">
          <h2>About This Tool</h2>
          <p>
            This pneumonia detection tool uses a deep learning model trained
            on chest X-ray images to identify signs of pneumonia. Simply upload
            a chest X-ray image, and click "Predict" to get the results.
          </p>
        </div>
      </div>
      <div id="ppreview-container">
        {previewSrc && <img id="preview" src={previewSrc} alt="Image preview" />}
        {result && <p id="result">Prediction: {result}</p>}
        {accuracy && <p id="accuracy">Confidence: {accuracy}</p>}
      </div>
    </div>
  );
};

const PneumoniaRoutes = () => {
  return (
    <Routes>
      <Route path="profile" element={<Profile />} />
      <Route path="history" element={<History />} />
      <Route path="/" element={<PneumoniaDetection />} />
    </Routes>
  );
};

export default PneumoniaRoutes;
