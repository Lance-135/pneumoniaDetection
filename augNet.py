from image.images import get_general_imageData, getCategoryImageData
from model.intro import model1,model3
from model.tflModel import tfModel
import numpy as np
import tensorflow as tf 
from tensorflow.keras.losses import BinaryCrossentropy # type: ignore
from tensorflow.keras.optimizers import Adam  # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore
import matplotlib.pyplot as plt


# Function to Train model 
def trainModel(model):
    # defining the data directories 
    train_dir  = "D:/AustinKarki/repos/inputData/train"
    test_dir  = "D:/AustinKarki/repos/inputData/test"
    saveName = input("Enter name of the model: ")

    # Creates an instance of ImageDataGenerator
    train_datagen = ImageDataGenerator(
        rescale=1./255,          # Normalizes the images
        rotation_range=10,       
        width_shift_range=0.1,   
        zoom_range=0.2,      
        brightness_range=[0.8, 1.2],   
        shear_range=0.2,
        vertical_flip = True,
        horizontal_flip=False,   
        fill_mode='nearest'      
    )

    # For validation or test data, Only rescaling is done 
    test_datagen = ImageDataGenerator(
        rescale=1./255,          # Normalizes the images
        )


    # Generates a batch of images
    train_generator = train_datagen.flow_from_directory(
        train_dir,      
        target_size=(500,500),   
        batch_size=8,             
        class_mode='binary',       
        color_mode='grayscale'     
    )

    validation_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(500,500),    
        batch_size=16,
        class_mode='binary',
        color_mode='grayscale'
    )   
    # Normal = 0, Pneumonia = 1 .. automatically assigned based on Alphabetical order
    # fit the data on the model 
    history = model.fit(
        train_generator, 
        steps_per_epoch = np.ceil(train_generator.samples / train_generator.batch_size),
        validation_data = validation_generator,
        validation_steps = np.ceil(validation_generator.samples / validation_generator.batch_size),
        epochs = 10
    )

    model.save(f"../trainedModels/model1/{saveName}.h5")
    plotData(history,saveName)


#Function to test the model on test data
def testModel():
    modelName = input("Enter model name: ")
    testData = get_general_imageData("val")
    x_test = np.array([dt[0] for dt in testData])
    y_test = np.array([dt[1] for dt in testData])
    x_test = x_test/255
    loaded_model = tf.keras.models.load_model(f"../trainedModels/model1/{modelName}.h5")
    loaded_model.evaluate(x_test, y_test)


# Predict Image class
def predictImage():
    modelName = input("Enter model name: ")
    data = getCategoryImageData("val", "NORMAL")
    x= np.array([dt[0] for dt in data])
    x = x/255
    loaded_model = tf.keras.models.load_model(f"../trainedModels/model1/{modelName}.h5")
    predict = loaded_model.predict(x)
    print(predict)


# plots the training results in a graph    
def plotData(history, saveName):
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title(f'{saveName} Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

trainModel(model3)