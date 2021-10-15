from tensorflow import keras
import tkinter as tk
from tkinter import filedialog

model = keras.models.load_model('path where you saved your model_keras')

import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing import image


root = tk.Tk()
root.withdraw()


uploaded = filedialog.askopenfilename(title = "Select a File")

#for fn in uploaded.keys():
 
  # predicting images
  #path = '/content/' + fn
img = image.load_img(str(uploaded), target_size=(200, 200))
x = image.img_to_array(img)
plt.imshow(x/255.)
x = np.expand_dims(x, axis=0)
images = np.vstack([x])
classes = model.predict(images, batch_size=10)
print(classes[0])
if classes[0]<0.5:
  print("Grab an umbrella. Rain is coming")
else:
  print("You're good to go. No rain is expected")