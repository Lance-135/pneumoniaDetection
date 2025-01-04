import tensorflow as tf

# create an instance of modelcheckpoint
def createCheckPoint(filepath):
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath= filepath,
        save_best_only= True,
        monitor = "val_accuracy",
        mode = "max",
        verbose= 1
    )
    return checkpoint_callback , checkpoint_callback.epochs_since_last_save

def imageGenerator():
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,          # Normalizes the images
        rotation_range=10,       
        width_shift_range=0.1,   
        zoom_range=0.2,      
        brightness_range=[0.7, 1.2],   
        shear_range=0.2,
        vertical_flip = True,
        horizontal_flip= False,   
        fill_mode='nearest'      
    )
    val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale= 1./255
    )
    return train_datagen, val_datagen