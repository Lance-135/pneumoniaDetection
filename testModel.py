from gc import callbacks
from image.images import get_general_imageData, getCategoryImageData
from model.intro import model1,model3
from tflModel import tfModel
import numpy as np
import tensorflow as tf 
from keras.losses import BinaryCrossentropy # type: ignore
from keras.optimizers import Adam  # type: ignore
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping # type: ignore
import matplotlib.pyplot as plt
import csv
from tools import createCheckPoint, imageGenerator

# Function to Train model 
def trainModel(model):
    # defining the data directories 

    train_dir  = "D:/AustinKarki/repos/inputData/train"
    test_dir  = "D:/AustinKarki/repos/inputData/test"
    saveName = input("Enter the model name: ")
    
    data = get_general_imageData("train")
    x = np.array([dt[0] for dt in data])
    y = np.array([dt[1] for dt in data])

    # call back functions   
    
    
    # creating checkpoint for the model
    filePath = f"../trainedModels/model3/{saveName}.h5" 
    filePath = f"../trainedModels/tfmodel/{saveName}.h5"
    checkpoint = createCheckPoint(filePath)

    history = tfModel.fit(
        x, 
        y,
        batch_size= 16, 
        epochs = 5, 
        callbacks= [checkpoint]
    )

    # plotData(history,saveName)
    # saveResults(history, saveName)

# plots the training results in a graph    
def plotData(history, saveName):
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title(f'{saveName} Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

def summary():
    modelName = input("Name the model to load: ")
    model = tf.keras.models.load_model(f"../trainedModels/model1/{modelName}.h5")
    model.summary()

def saveResults(history, saveName):
    trainLoss = history.history['loss'][-1]
    trainAcc = history.history["accuracy"][-1]
    valLoss = history.history["val_loss"][-1]
    valAcc = history.history["val_accuracy"][-1]
    with open("results.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([
            saveName,
            f"train_acc: {trainAcc: 0.4f}", 
            f"train_loss: {trainLoss: 0.4f}", 
            f"val_acc: {valAcc: 0.4f}",
            f"val_loss: {valLoss: 0.4f}"])
# summary()
trainModel(tfModel)
