#__________LIBRARIES__________
import os
import requests
import pandas as pd
import json
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

from datetime import date
from datetime import timedelta

from tensorflow import keras
from tkinter import filedialog

from keras.preprocessing import image

#____________DATE___________
today = date.today()
past = today + timedelta(days=-7)


#__________TENSORFLOW MESSAGES DURING RUN____________
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  #set to 3 to avoid tensorflow messages (https://stackoverflow.com/questions/35911252/disable-tensorflow-debugging-information/42121886#42121886)


#__________DATASETS__________ 
dataCities = pd.read_csv('dataCities.csv') #dataset with IPMA city codes


#__________API__________
#open weather API
open_api_key = 'enter here your access key' #access Open Weather API; You must register to get an access key: https://openweathermap.org

#newsapi API
news_api = 'enter here your access key' # access newsapi API; You must register to get an access key: https://newsapi.org


#___________INPUTS__________
root = tk.Tk()
root.withdraw()


uploaded = filedialog.askopenfilename(title = "Select a File")


user_input = input("Em que cidade está? ")
while user_input not in list(dataCities['local']):
    user_input = input("Lamentamos. Apenas estão disponíveis capitais de distrito (ex. Vila Real): ")


#__________MODEL__________
model = keras.models.load_model('insert here the path for the model') #path where the model is saved e.g. /Users/user/project/keras_model


img = image.load_img(str(uploaded), target_size=(200, 200))  #load and resize image
x = image.img_to_array(img) #conver image to array
plt.imshow(x/255.)
x = np.expand_dims(x, axis=0)
images = np.vstack([x])
classes = model.predict(images, batch_size=10)
#print(classes[0])
if classes[0]<0.5:
  print("Resultado da imagem: \n Agarre um guarda-chuva. Vai chover")
else:
  print("Resultado da imagem: \n É seguro sair. Não vai chover")

print()

#__________IPMA SERVICE__________

def local_to_code(user_input):
    ipmaCode = list(dataCities[dataCities['local'] == user_input]['globalIdLocal'])[0] #converts city to IPMA code
    ipmaGet = requests.get(f"https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/"+str(ipmaCode)+".json") #do request to IPMA API with the code of the city already embeded
    ipmaWeather = ipmaGet.content #search the content wich is a list of dictionaries 
    return json.loads(ipmaWeather.decode('utf-8'))['data'][0]['precipitaProb'] #returns precipitation probability only

print(f"Hoje, a probabilidade de chuva em {user_input} é de: " + local_to_code(user_input) + "%.")


#__________OPEN WEATHER SERVICE__________

weather_data = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&appid={open_api_key}&lang=pt") #do request to open weather API

if weather_data.json()['cod'] == '404': #error message to city not found
    print('No city found')
else:
    weather = weather_data.json()['weather'][0]['description']
    temp = round(weather_data.json()['main']['temp'])
    humid = weather_data.json()['main']['humidity']
    wind = round(weather_data.json()['wind']['speed'])
    maxTemp = round(weather_data.json()['main']['temp_max'])
    minTemp = round(weather_data.json()['main']['temp_min'])


    print(f"Nesta altura, o tempo na cidade {user_input} é {weather}. \n A temperatura é de {temp} ºC com {humid} % de humidade. \n O vento sopra a {wind} km/h. \n A temperatura máxima é de: {maxTemp} ºC \n A temperatura mínima é de: {minTemp} ºC")

print()


#___________NEWS SERVICE__________
newsInfo = requests.get(
    f"https://newsapi.org/v2/everything?q={user_input}&language=pt&from={past}&to={today}&pageSize=3&apiKey={news_api}"
)

#1st news headline
newsTitle1 = newsInfo.json()['articles'][0]['title']
newsLead1 = newsInfo.json()['articles'][0]['description']
newsLink1 = newsInfo.json()['articles'][0]['url']

#2nd news headline
newsTitle2 = newsInfo.json()['articles'][1]['title']
newsLead2 = newsInfo.json()['articles'][1]['description']
newsLink2 = newsInfo.json()['articles'][1]['url']

#3rd news headline
newsTitle3 = newsInfo.json()['articles'][2]['title']
newsLead3 = newsInfo.json()['articles'][2]['description']
newsLink3 = newsInfo.json()['articles'][2]['url']

#show results
print(f"As notícias mais recentes para {user_input}: \n {newsTitle1} \n {newsLead1} \n Mais informação: \n {newsLink1} \n\n")
print(f"{newsTitle2} \n {newsLead2} \n Mais informação: \n {newsLink2} \n\n")
print(f"{newsTitle3} \n {newsLead3} \n Mais informação: \n {newsLink3} \n\n")