from flask import Flask, request, jsonify
from flask_cors import CORS #libray for tensorflow connection 
import numpy as np
import tensorflow as tf
from PIL import Image
import os
from tensorflow.compat.v1 import ConfigProto, Session # type: ignore


config = ConfigProto()
config.gpu_options.allow_growth = True 
session = Session(config=config)
tf.compat.v1.keras.backend.set_session(session)
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


model = tf.keras.models.load_model('../trainedModels/model1/model40.h5')


def crop_outer_20_percent(image_path):
    # Open the image
    image = Image.open(image_path).convert('L')
    width, height = image.size

    # Calculate the crop margin (20% of width and height)
    margin_width = int(0.1 * width)
    margin_height = int(0.1 * height)

    # Define the crop box
    left = margin_width
    upper = margin_height   
    right = width - margin_width
    lower = height - margin_height

    # Crop the image
    cropped_image = image.crop((left, upper, right, lower))
    return cropped_image

def preprocess_image(image_path):
    """Preprocess the uploaded image to match the model's input shape."""
    # Convert to grayscale
    # image = Image.open(image_path).convert('L') 
    image = crop_outer_20_percent(image_path)
    image = image.resize((256, 256))  
    image_array = np.array(image) / 255.0  
    image_array = np.expand_dims(image_array, axis=(0, -1)) 
    print(image_array.shape) 
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
    result = "Pneumonia Detected" if prediction > 0.5 else "NORMAL"
    print("prediction: ", prediction)
    accuracy = prediction if prediction > 0.5 else 1 - prediction 

    return jsonify({'result': result, 'accuracy': f"{accuracy: 0.4f}"})



if __name__ == '__main__':
    app.run(debug=True)
