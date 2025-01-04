from doctest import testmod
from gc import callbacks
from tabnanny import verbose

import test
from image.images import get_general_imageData, getCategoryImageData
from model.intro import model1,model2,model3
import numpy as np
import tensorflow as tf 
from tensorflow.keras.losses import BinaryCrossentropy # type: ignore
from tensorflow.keras.optimizers import Adam  # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore
import matplotlib.pyplot as plt

#Function to train model 
def trainModel(modelName, saveName): 
    #load training and cross validation data from the directory
    trainData = get_general_imageData("train")
    valData = get_general_imageData("val")

    #seperating the image data and labels 
    x_train = np.array([dt[0] for dt in trainData])
    y_train = np.array([dt[1] for dt in trainData])
    x_val = np.array([dt[0] for dt in valData])
    y_val = np.array([dt[1] for dt in valData])
    
    history = modelName.fit(
        x_train, 
        y_train, 
        epochs=20, 
        batch_size=8, 
        validation_data=(x_val, y_val) 
    )
    # Save in HDF5 format
    modelName.save(f"../trainedModels/{saveName}.h5")  

    # plot data
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()



#Function to test the model on test data
def testModel(name):
    testData = get_general_imageData("test")
    x_test = np.array([dt[0] for dt in testData])
    y_test = np.array([dt[1] for dt in testData])
    x_test = x_test/255
    loaded_model = tf.keras.models.load_model(f"../trainedModels/{name}.h5")
    loaded_model.evaluate(x_test, y_test)

def predictImage(modelName):
    data = getCategoryImageData("val", "PNEUMONIA")
    x= np.array([dt[0] for dt in data])
    x = x/255
    loaded_model = tf.keras.models.load_model(f"../trainedModels/{modelName}.h5")
    predict = loaded_model.predict(x)
    print(predict)

model1.summary()
'''
# class to describe a neural network
class Network:

    def __init__(self,model):
        self.model = model 

    @property
    def model(self):
        return self.model 
    @model.setter
    def model(self, model):
        self._model = model
    
    #model summary
    def summary(self):
        return self.model.summary()
    
    # Method to compile the model 
    def compile(self):
        return self.model.compile(optimizer = Adam(0.0001), loss = BinaryCrossentropy(), metrics = ["accuracy"])

    # Method to train model     
    def trainModel(self, saveName): 
        #load training and cross validation data from the directory
        trainData = get_general_imageData("train")
        valData = get_general_imageData("val")

        #seperating the image data and labels 
        x_train = np.array([dt[0] for dt in trainData])
        y_train = np.array([dt[1] for dt in trainData])
        x_val = np.array([dt[0] for dt in valData])
        y_val = np.array([dt[1] for dt in valData])
        history = self.model.fit(
            x_train, 
            y_train, 
            epochs=7, 
            batch_size=4, 
            validation_data=(x_val, y_val)
        )
        j_trainFinal = self.model.evaluate(x_train, y_train, verbose = 0)
        j_cvFinal = self.model.evaluate(x_val, y_val, verbose = 0)
        # Save in HDF5 format
        self.model.save(f"model/{saveName}.h5") 

    # Method to test model 
    def testModel(name):
        testData = get_general_imageData("test")
        x_test = np.array([dt[0] for dt in testData])
        y_test = np.array([dt[1] for dt in testData])
        loaded_model = tf.keras.models.load_model(f"model/{name}.h5")
        loss = loaded_model.evaluate(x_test, y_test)
        return loss
'''