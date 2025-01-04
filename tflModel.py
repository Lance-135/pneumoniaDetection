import tensorflow as tf
from keras.applications import VGG16 # type: ignore
from keras.layers import Dense, Flatten, Dropout # type: ignore
from keras.models import Sequential # type: ignore
from keras.preprocessing.image import ImageDataGenerator #type: ignore 
from keras.optimizers import Adam #type: ignore 
from keras.losses import BinaryCrossentropy #type: ignore 

# Load the pre-trained VGG16 model without the top layers (classifier part)
baseModel = tf.keras.applications.VGG16(weights = "imagenet", include_top = False, input_shape = (224, 224, 3))


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
# tfModel.summary()
