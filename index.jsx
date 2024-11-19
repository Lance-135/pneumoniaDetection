import React, { useState } from "react";


const PneumoniaDetection = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewSrc, setPreviewSrc] = useState("");
  const [result, setResult] = useState("");
  const [accuracy, setAccuracy] = useState("");

  
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreviewSrc(e.target.result);
        setResult(""); // Clear the result
        setAccuracy(""); // Clear the accuracy
      };
      reader.readAsDataURL(file);
    }
  };

  const handlePrediction = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("image", selectedFile);
    const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 seconds

    try {
      setResult("Processing...");
      setAccuracy(""); // Reset accuracy during processing
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
        signal: controller.signal,
      });
      clearTimeout(timeoutId); // Clear timeout if successful
      const data = await response.json();
      setResult(data.result || "Error processing the image");
      setAccuracy(data.accuracy ? `${(data.accuracy * 100).toFixed(2)}%` : "");
      
      setResult(data.result || "Error processing the image");
    } catch (error) {
      setResult("Error connecting to the server");
    }
  };

  return (
    <div id="ccontainer">
      <header>Pneumonia Detection</header>
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
            on chest X-ray images to identify signs of pneumonia. Simply
            upload a chest X-ray image, and click "Predict" to get the results.
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

export default PneumoniaDetection;
