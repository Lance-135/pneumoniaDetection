import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import "./index.css";

const History = () => {
    const [predictions, setPredictions] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [currentPredictionId, setCurrentPredictionId] = useState(null);
    const [reviewerName, setReviewerName] = useState("");
    const [category, setCategory] = useState("");

    const email = localStorage.getItem("userEmail");

    useEffect(() => {
        fetchPredictions();
    }, [email]);

    const fetchPredictions = () => {
        axios.get(`http://localhost:3001/history/${email}`)
            .then(res => setPredictions(res.data))
            .catch(err => console.error("Error loading history:", err));
    };

    const openModal = (predictionId) => {
        setCurrentPredictionId(predictionId);
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
        setReviewerName("");
        setCategory("");
    };

    const handleSubmit = async () => {
        if (!reviewerName || !category) {
            alert("Both reviewer name and category are required.");
            return;
        }
        try {
            await axios.post(`http://localhost:3001/radiologist-feedback/${email}/${currentPredictionId}`, {
                decision: category,
                reviewedBy: reviewerName,
            });
            alert("Feedback submitted successfully!");
            fetchPredictions(); // Refresh data
            closeModal();
        } catch (error) {
            alert("Error submitting feedback.");
        }
    };

    const handleDelete = async (predictionId) => {
        try {
            await axios.delete(`http://localhost:3001/delete-prediction/${email}/${predictionId}`);
            alert("Prediction deleted successfully!");
            setPredictions(predictions.filter(p => p._id !== predictionId));
        } catch (error) {
            alert("Error deleting prediction.");
        }
    };

    return (
        <div className="history-container">
            <h2>Prediction History</h2>
            {predictions.map((prediction, index) => (
                <div
                    key={index}
                    className="prediction-item"
                    onClick={() => openModal(prediction._id)}
                    style={{ cursor: "pointer" }}
                >
                    <img src={prediction.image} alt={`Prediction ${index}`} style={{ maxWidth: "100px" }} />
                    <p><strong>Result:</strong> {prediction.result}</p>
                    <p><strong>Confidence:</strong> {prediction.confidence}%</p>
                    {prediction.radiologistFeedback ? (
                        <>
                            <p><strong>Category:</strong> {prediction.radiologistFeedback.decision}</p>
                            <p><strong>Reviewed by:</strong> {prediction.radiologistFeedback.reviewedBy}</p>
                        </>
                    ) : (
                        <p><em>Click to provide feedback</em></p>
                    )}
                    <button onClick={(e) => {
                        e.stopPropagation();
                        handleDelete(prediction._id);
                    }}>Delete</button>
                </div>
            ))}
            <Link to="/index" className="back-button">Back to Home</Link>

            {showModal && (
                <div className="modal">
                    <div className="modal-content">
                        <h3>Provide Feedback</h3>
                        <label>
                            Reviewer Name:
                            <input
                                type="text"
                                value={reviewerName}
                                onChange={(e) => setReviewerName(e.target.value)}
                            />
                        </label>
                        <label>
                            Category:
                            <select value={category} onChange={(e) => setCategory(e.target.value)}>
                                <option value="">Select...</option>
                                <option value="Confirmed Pneumonia">Confirmed Pneumonia</option>
                                <option value="No Pneumonia">No Pneumonia</option>
                            </select>
                        </label>
                        <button onClick={handleSubmit}>Submit</button>
                        <button onClick={closeModal}>Cancel</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default History;
