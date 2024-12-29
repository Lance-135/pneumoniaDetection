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
    
    pneumonia_data = getCategoryImageData("train", "PNEUMONIA")
    normal_data = getCategoryImageData("train", "NORMAL")

    xn_train = np.array([dt[0] for dt in normal_data])
    yn_train = np.array([dt[1] for dt in normal_data])

    augmentedData = []
    train_gen, val_gen = imageGenerator()
    for image in xn_train:
        image = np.expand_dims(image, axis= 0)
        for _ in range(2):
            augImg = train_gen.flow(image, batch_size=1).next()[0]
            augmentedData.append((augImg, 0))
    
    print(len(augmentedData))


 
    
    # call back functions   
    # instance of early stopping 
    # earlyStopping = EarlyStopping(
    #     monitor = "val_loss",
    #     patience = 5,
    #     restore_best_weights = True
    # )
    
    #creating checkpoint for the model
    # filePath = f"../trainedModels/model3/{saveName}.h5" 
    # filePath = f"../trainedModels/tfmodel/{saveName}.h5"
    # checkpoint = createCheckPoint(filePath)

    # Normal = 0, Pneumonia = 1 .. automatically assigned based on Alphabetical order
    # fit the data on the model 
    # history = model.fit(
    #     # train_generator, 
    #     steps_per_epoch = np.ceil(train_generator.samples / train_generator.batch_size),
    #     validation_data = validation_generator,
    #     validation_steps = np.ceil(validation_generator.samples / validation_generator.batch_size),
    #     epochs = 5,
    #     callbacks = [checkpoint],
    # )

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
