from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from PIL import Image
import os
from tensorflow.compat.v1 import ConfigProto, Session

config = ConfigProto()
config.gpu_options.allow_growth = True  # Only allocate memory as needed
session = Session(config=config)
tf.compat.v1.keras.backend.set_session(session)
app = Flask(__name__)

# Create an upload directory if it doesn't exist
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load your model (update the path accordingly)
model = tf.keras.models.load_model('../trainedModels/model40.h5')

def preprocess_image(image_path):
    """Preprocess the uploaded image to match the model's input shape."""
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image = image.resize((256, 256))  # Resize to 256x256
    image_array = np.array(image) / 255.0  # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=(0, -1))  # Add batch and channel dimensions
    return image_array

@app.route('/')
def home():
    """Root route that provides information about the API."""
    return jsonify({
        'message': 'Welcome to the Pneumonia Detection API!',
        'routes': {
            'POST /predict': 'Upload an image to get a prediction',
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Route to handle pneumonia predictions."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)

    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)

    # Make a prediction
    prediction = model.predict(preprocessed_image)[0][0]  
    result = "Pneumonia Detected" if prediction > 0.5 else "No Pneumonia"
    accuracy = prediction if prediction > 0.5 else 1 - prediction  
    print(result, accuracy)
    return jsonify({'result': result, 'accuracy': accuracy})



if __name__ == '__main__':
    app.run(debug=True)
