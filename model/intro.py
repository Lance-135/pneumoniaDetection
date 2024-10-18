import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dense, Dropout # type: ignore
from tensorflow.keras.losses import BinaryCrossentropy # type: ignore
from tensorflow.keras.optimizers import Adam# type: ignore

reg1 = 0.01

model1 = Sequential([
    tf.keras.Input(shape = (500,500,1)),

    # Convolutional Layers
    Conv2D(filters = 32, kernel_size = (3,3), activation = "relu", kernel_regularizer = tf.keras.regularizers.l2(0.01)),
    MaxPooling2D(pool_size =(2,2) ),
    Conv2D(filters = 64, kernel_size = (3,3), activation = "relu"),
    MaxPooling2D(pool_size = (2,2)),
    Conv2D(filters = 128, kernel_size = (3,3), activation = "relu"),
    MaxPooling2D(pool_size = (2,2)),
    # Conv2D(filters = 256, kernel_size = (3,3), activation = "relu", kernel_regularizer=tf.keras.regularizers.l2(reg1)),
    # MaxPooling2D(pool_size = (2,2)),

    Flatten(),

    # Dense Layers
    Dense(units = 64, activation = "relu",  kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    Dense(units = 32, activation = "relu" ,kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    Dense(units = 8, activation = "relu" ,kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    
    # Output Layer
    Dense(units = 1, activation = "sigmoid")

])

model1.compile(optimizer = Adam(0.001), loss = BinaryCrossentropy(), metrics = ["accuracy"])




model2 = Sequential([
    tf.keras.Input(shape=(500,500,1)),
    Conv2D(filters = 64, kernel_size = (3,3), activation = "relu"),
    MaxPooling2D(pool_size = (2,2)),
    Conv2D(filters = 32, kernel_size = (3,3), activation = "relu"),
    MaxPooling2D(pool_size= (2,2)),

    Flatten(),

    Dense(units = 32, activation = "relu", kernel_regularizer = tf.keras.regularizers.l2(0.001)),
    Dense(units = 16,activation = "relu", kernel_regularizer = tf.keras.regularizers.l2(0.001)),
    Dense(units = 8, activation = "relu", kernel_regularizer = tf.keras.regularizers.l2(0.001)),
    Dense(units = 1 , activation = "sigmoid")
])
 
model2.compile(optimizer = Adam(0.001), loss = BinaryCrossentropy(), metrics = ["accuracy"])



model3 = Sequential([
    tf.keras.Input(shape=(900,900,1)),
    Conv2D(filters = 40, kernel_size = (3,3), activation = "relu"),
    MaxPooling2D(pool_size = (2,2)),
    Conv2D(filters = 16, kernel_size = (3,3), activation = "relu"),
    MaxPooling2D(pool_size= (2,2)),

    Flatten(),

    Dense(units = 32, activation = "relu", kernel_regularizer = tf.keras.regularizers.l2(0.001)),
    Dense(units = 16,activation = "relu", kernel_regularizer = tf.keras.regularizers.l2(0.001)),
    Dense(units = 8, activation = "relu", kernel_regularizer = tf.keras.regularizers.l2(0.001)),
    Dense(units = 1 , activation = "sigmoid")
])

model3.compile(optimizer = Adam(0.001), loss = BinaryCrossentropy(), metrics = ["accuracy"])