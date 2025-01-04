from random import shuffle
import cv2
import glob
import numpy as np
import random as rd
from tools import imageGenerator
from PIL import Image


# Get a list of touple with the (image in grayscale, 0 or 1)
def getCategoryImageData(type, category ):
    folder_path = f"D:/AustinKarki/repos/inputData/{type}/{category}/*.*"  
    # folder_path = "D:/AustinKarki/repos/inputData/fromWeb/pn/*.*"  
    #initializing an empty array
    imgData= []
    # Get a list of all image files in the folder
    image_files = glob.glob(folder_path)
    # Loop through the image files
    for file in image_files:
        # using openCv
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        img_resized = cv2.resize(img, (256,256))
        # img_resized = cv2.resize(img, (224,224)) # (224, 224) for vgg16
        img_3d = np.expand_dims(img_resized, axis = -1) 
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


def augmentedImages(type, category):
    normal_data = getCategoryImageData(type, category)
    xn_train = np.array([dt[0] for dt in normal_data])

    augmentedData = []
    train_gen, val_gen = imageGenerator()
    for image in xn_train:
        image = np.expand_dims(image, axis= 0)
        for _ in range(2):                                      # 2 for doubling the original number of normal images
            augImg = train_gen.flow(image, batch_size=1).next()[0]
            augmentedData.append((augImg, 0))
    return augmentedData
