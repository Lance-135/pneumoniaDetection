import tensorflow as tf
from tensorflow.keras.applications import VGG16 # type: ignore
from tensorflow.keras.layers import Dense, Flatten, Dropout # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator #type: ignore 
from tensorflow.keras.optimizers import Adam #type: ignore 
from tensorflow.keras.losses import BinaryCrossentropy #type: ignore 

# Load the pre-trained VGG16 model without the top layers (classifier part)
baseModel = tf.keras.applications.VGG16(weights = "imagenet", include_top = False, input_shape = (256, 256, 3))


# Freeze the layers of base model 
for layer in baseModel.layers:
    layer.trainable = False

tfModel = Sequential([
    baseModel, 
    Flatten(),
    # Dense Layers
    Dense(units = 256 , activation = "relu", kernel_regularizer = tf.keras.regularizers.l2(0.001)),
    Dense(units = 1, activation = "sigmoid")
])


tfModel.compile(optimizer = Adam(0.001), loss = BinaryCrossentropy(), metrics = ['accuracy'])

