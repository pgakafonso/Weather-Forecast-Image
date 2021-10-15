#__________LIBRARIES__________
import keras as k 
import os
import tensorflow as tf
import numpy as np
import tkinter as tk
from tkinter import filedialog

 

from tensorflow.keras.preprocessing.image import ImageDataGenerator

from itertools import cycle

from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
from sklearn.metrics import roc_auc_score


#__________NOTES__________

#Had to install protobuf (pip install on ironhack environment) 
#because this was giving me the error in this link: 
# https://stackoverflow.com/questions/67570696/typeerror-parameter-to-mergefrom-must-be-instance-of-same-class-expected-ten


# Directory with our training cloud pictures
train_cloud_dir = os.path.join('path for training images of clouds')

# Directory with our training clear pictures
train_clear_dir = os.path.join('path for training images of clear')

# Directory with our validation cloud pictures
valid_cloud_dir = os.path.join('path for validation images of clouds')

# Directory with our validation clear pictures
valid_clear_dir = os.path.join('path for validation images of clear')




#__________CONTINUE___________

# All images will be rescaled by 1./255
train_datagen = ImageDataGenerator(rescale=1/255)
validation_datagen = ImageDataGenerator(rescale=1/255)

# Flow training images in batches of 3 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
        'path for training images folder',  # This is the source directory for training images
        classes = ['cloud', 'clear'],
        target_size=(200, 200),  # All images will be resized to 200x200
        batch_size=10,
        # Use binary labels
        class_mode='binary')

# Flow validation images in batches of 2 using valid_datagen generator
validation_generator = validation_datagen.flow_from_directory(
        'path for validation images folder',  # This is the source directory for validation images
        classes = ['cloud', 'clear'],
        target_size=(200, 200),  # All images will be resized to 200x200
        batch_size=5,
        # Use binary labels
        class_mode='binary',
        shuffle=False)

model = tf.keras.models.Sequential([tf.keras.layers.Flatten(input_shape = (200,200,3)), 
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu), 
                                    tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)])


model.compile(optimizer = tf.optimizers.Adam(),
              loss = 'binary_crossentropy',
              metrics=['accuracy'])


history = model.fit(train_generator,
      steps_per_epoch=10,  
      epochs=15,
      verbose=1,
      validation_data = validation_generator,
      validation_steps=10) #-> number of validation steps must be lower than number of images on validation folder

model.save('path where you want to save your model_keras, best practice to save it on the same folder where you have your project (py app, etc.)')