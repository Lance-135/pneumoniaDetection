from random import shuffle
import cv2
import glob
import numpy as np
import random as rd
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore


# Get a list of touple with the (image in grayscale, 0 or 1)
def getCategoryImageData(type, category ):
    folder_path = f"D:/AustinKarki/repos/inputData/{type}/{category}/*.jpeg"  # Change to '*.jpg' or any other extension
    #initializing an empty array
    imgData= []
    # Get a list of all image files in the folder
    image_files = glob.glob(folder_path)

    # Loop through the image files
    for file in image_files:
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        img_resized = cv2.resize(img, (500,500))
        img_3d = np.expand_dims(img_resized, axis = -1) # for other models
        # img_3d= cv2.cvtColor(img_resized, cv2.COLOR_GRAY2RGB) #for tfModel
        if category== "NORMAL":
            imgData.append((img_3d,0))
        else:
            imgData.append((img_3d,1))
    return imgData



def get_general_imageData(type):
    finalImageList = getCategoryImageData(type, "NORMAL") + getCategoryImageData(type, "PNEUMONIA")
    # rd.shuffle(finalImageList)
    return finalImageList


def matrixToImage():
    data = getCategoryImageData("val", "NORMAL")
    x = np.array([dt[0] for dt in data])
    cv2.imshow('Grayscale Image', x[1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
