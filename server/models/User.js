const mongoose = require('mongoose');

const PredictionSchema = new mongoose.Schema({
    image: String,
    result: String,
    confidence: Number,
    radiologistFeedback: {
        decision: String,
        reviewedBy: String,
        date: { type: Date, default: Date.now },
    },
});

const UserSchema = new mongoose.Schema({
    name: String,
    email: { type: String, unique: true },
    password: String,
    gender: String,
    address: String,
    phone: String,
    predictions: [PredictionSchema],
});

const UserModel = mongoose.model("users", UserSchema);
module.exports = UserModel;
