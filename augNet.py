from gc import callbacks
from image.images import get_general_imageData, getCategoryImageData
from model.intro import model1,model3
from tflModel import tfModel
import numpy as np
import tensorflow as tf 
from keras.losses import BinaryCrossentropy # type: ignore
from keras.optimizers import Adam  # type: ignore
from keras.preprocessing.image import ImageDataGenerator  # type: ignore
from keras.callbacks import EarlyStopping # type: ignore
import matplotlib.pyplot as plt
import csv
from tools import createCheckPoint, imageGenerator

# Function to Train model 
def trainModel(model):
    # defining the data directories 

    train_dir  = "D:/AustinKarki/repos/inputData/train"
    test_dir  = "D:/AustinKarki/repos/inputData/test" 
    #mero path
    # train_dir  = "D:/College/Sixth_sem/project/chest_xray/train"
    # test_dir  = "D:/College/Sixth_sem/project/chest_xray/test" 
    saveName = input("Enter the model name: ")

    # Creates an instance of ImageDataGenerator
    train_datagen, test_datagen = imageGenerator()


    # Generates a batch of images
    train_generator = train_datagen.flow_from_directory(
        train_dir,      
        target_size=(256,256),   
        # target_size=(224, 224), # for vgg16   
        batch_size=16,             
        class_mode='binary',       
        color_mode='grayscale'     # for tf model color mode is rgb so 
        # color_mode= "rgb"
    )

    validation_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(256,256),    
        # target_size=(224, 224),    # for vgg16
        batch_size=16,
        class_mode='binary',
        color_mode='grayscale' # For normal model 
        # color_mode= "rgb"
    )
    # call back functions   
    # instance of early stopping 
    earlyStopping = EarlyStopping(
        monitor = "val_loss",
        patience = 5,
        restore_best_weights = True
    )
    
    #creating checkpoint for the model
    filePath = f"../trainedModels/model3/{saveName}.h5" 
    # filePath = f"../trainedModels/tfmodel/{saveName}.h5"
    checkpoint, epoch_since_last_save = createCheckPoint(filePath)

    # Normal = 0, Pneumonia = 1 .. automatically assigned based on Alphabetical order
    # fit the data on the model 
    history = model.fit(
        train_generator, 
        steps_per_epoch = np.ceil(train_generator.samples / train_generator.batch_size),
        validation_data = validation_generator,
        validation_steps = np.ceil(validation_generator.samples / validation_generator.batch_size),
        epochs = 20,
        callbacks = [checkpoint],
    )

    plotData(history,saveName)
    saveResults(history, saveName, epoch_since_last_save)


#Function to test the model on test data
def testModel():
    modelName = input("Enter model name: ")
    data = get_general_imageData("train")
    x = np.array([dt[0]/255 for dt in data])
    y = np.array([dt[1] for dt in data])
    ndata = getCategoryImageData("test", "NORMAL")
    pdata = getCategoryImageData("test", "PNEUMONIA")
    # data = get_general_imageData("test")
    xn= np.array([dt[0] for dt in ndata])
    print(xn.shape)
    xn = xn/255
    xp = np.array([dt[0] for dt in pdata])
    xp = xp/255
    loaded_model = tf.keras.models.load_model(f"../trainedModels/model1/{modelName}.h5")
    print(loaded_model.evaluate(x,y))
    predict = loaded_model.predict(xn)
    n = 0
    p = 0
    for prediction in predict:
        if prediction[0] < 0.5:
            n +=1
    print(f"total normal images: {len(xn)}, classified as normal: {n}")
    predict = loaded_model.predict(xp)
    for prediction in predict:
        if prediction[0] > 0.5:
            p +=1
    print(f"total PNEUMONIA images: {len(xp)}, classified as PNEUMONIA: {p}")



# Predict Image class
def predictImage():
    modelName = input("Enter the model name: ")
    data = getCategoryImageData("input", "PNEUMONIA")
    x = np.array([dt[0] for dt in data])
    x = x/255
    print(x.shape)
    loaded_model = tf.keras.models.load_model(f"../trainedModels/model1/{modelName}.h5")
    # loaded_model.summary()
    predict = loaded_model.predict(x)   
    print(predict)
   

# plots the training results in a graph    
def plotData(history, saveName):
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.xticks(range(0, 21))
    plt.show()

def summary():
    modelName = input("Name the model to load: ")
    model = tf.keras.models.load_model(f"../trainedModels/model1/{modelName}.h5")
    model.summary()

def saveResults(history, saveName, n):
    trainLoss = history.history['loss'][-(n-1)]
    trainAcc = history.history["accuracy"][-(n-1)]
    valLoss = history.history["val_loss"][-(n-1)]
    valAcc = history.history["val_accuracy"][-(n-1)]
    with open("results.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([
            saveName,
            f"train_acc: {trainAcc: 0.4f}", 
            f"train_loss: {trainLoss: 0.4f}", 
            f"val_acc: {valAcc: 0.4f}",
            f"val_loss: {valLoss: 0.4f}"])
# summary()
# trainModel(model3)
# testModel()
predictImage()
