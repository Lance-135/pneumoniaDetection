const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const UserModel = require("./models/User");

const app = express();
app.use(express.json({ limit: "50mb" }));
app.use(cors());

mongoose.connect("mongodb://127.0.0.1:27017/User")
    .then(() => console.log("MongoDB connected successfully"))
    .catch((error) => console.error("MongoDB connection error:", error));

// User Signup Route
app.post("/signup", async (req, res) => {
    const { name, email, password } = req.body;
    try {
        const existingUser = await UserModel.findOne({ email });
        if (existingUser) {
            return res.status(400).json({ error: "User already exists" });
        }
        const newUser = await UserModel.create({ name, email, password });
        res.json(newUser);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});


app.post("/login",(req,res) => {
    const {email,password} = req.body;
    UserModel.findOne({email: email})
    .then(user => {
        if(user) {
            if(user.password === password){
                res.json("Success")
            } else {
                res.json("the password is incorrect")
            } 
        } else {
            res.json("No record existed")
        }
    })
});

// Fetch User Profile Route (Display All Entities)
app.get('/profile/:email', async (req, res) => {
    const { email } = req.params;
    try {
        const user = await UserModel.findOne({ email });
        if (user) {
            res.json(user);
        } else {
            res.status(404).json({ error: "User not found" });
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Update User Profile Route (Allow Editing Profile Fields)
app.put('/profile/:email', async (req, res) => {
    const { email } = req.params;
    const { name, address, phone, gender } = req.body;
    try {
        const updatedUser = await UserModel.findOneAndUpdate(
            { email },
            { name, address, phone, gender },
            { new: true }
        );
        res.json(updatedUser);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Store Prediction Result
app.post('/save-prediction/:email', async (req, res) => {
    const { email } = req.params;
    const { image, result, confidence } = req.body;
    try {
        const user = await UserModel.findOne({ email });
        if (!user) {
            return res.status(404).json({ error: "User not found" });
        }
        user.predictions.push({ image, result, confidence });
        await user.save();
        res.json({ message: "Prediction saved successfully" });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Fetch User Prediction History
app.get('/history/:email', async (req, res) => {
    const { email } = req.params;
    try {
        const user = await UserModel.findOne({ email });
        if (!user) {
            return res.status(404).json({ error: "User not found" });
        }
        res.json(user.predictions);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Radiologist Feedback Update
app.post('/radiologist-feedback/:email/:predictionId', async (req, res) => {
    const { email, predictionId } = req.params;
    const { decision, reviewedBy } = req.body;
    try {
        const user = await UserModel.findOne({ email });
        if (!user) {
            return res.status(404).json({ error: "User not found" });
        }
        const prediction = user.predictions.id(predictionId);
        if (!prediction) {
            return res.status(404).json({ error: "Prediction not found" });
        }
        prediction.radiologistFeedback = { decision, reviewedBy, date: new Date() };
        await user.save();
        res.json({ message: "Radiologist feedback submitted successfully." });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Delete a Prediction
app.delete('/delete-prediction/:email/:predictionId', async (req, res) => {
    const { email, predictionId } = req.params;
    try {
        const user = await UserModel.findOne({ email });
        if (!user) {
            return res.status(404).json({ error: "User not found" });
        }
        const predictionIndex = user.predictions.findIndex(p => p._id.toString() === predictionId);
        if (predictionIndex === -1) {
            return res.status(404).json({ error: "Prediction not found" });
        }
        user.predictions.splice(predictionIndex, 1);
        await user.save();
        res.json({ message: "Prediction deleted successfully." });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});


app.listen(3001, () => {
    console.log("Server running at http://localhost:3001");
});
