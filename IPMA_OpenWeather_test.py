#__________LIBRARIES__________

import requests
import pandas as pd
import json


#__________DATASETS__________ 
dataCities = pd.read_csv('dataCities.csv') #dataset with IPMA city codes


#___________OTHER__________
open_api_key = 'enter here your access key' #access Open Weather API; You must register to get an access key: https://openweathermap.org

user_input = input("Escolha uma cidade: ")
while user_input not in list(dataCities['local']):
    user_input = input("Escolha uma capital de distrito portuguesa (ex. Vila Real): ")


#__________IPMA SERVICE__________

def local_to_code(user_input):
    ipmaCode = list(dataCities[dataCities['local'] == user_input]['globalIdLocal'])[0] #converts city to IPMA code
    ipmaGet = requests.get(f"https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/"+str(ipmaCode)+".json") #do request to IPMA API with the code of the city already embeded
    ipmaWeather = ipmaGet.content #search the content wich is a list of dictionaries 
    return json.loads(ipmaWeather.decode('utf-8'))['data'][0]['precipitaProb'] #returns precipitation probability only

print(f"Hoje, a probabilidade de precipitação na cidade {user_input} é de: " + local_to_code(user_input) + "%.")


#__________OPEN WEATHER SERVICE__________

weather_data = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&appid={open_api_key}&lang=pt") #do request to open weather API

if weather_data.json()['cod'] == '404':
    print('A cidade não existe')
else:
    weather = weather_data.json()['weather'][0]['description']
    temp = round(weather_data.json()['main']['temp'])
    humid = weather_data.json()['main']['humidity']
    wind = round(weather_data.json()['wind']['speed'])
    maxTemp = round(weather_data.json()['main']['temp_max'])
    minTemp = round(weather_data.json()['main']['temp_min'])


    print(f"O tempo na cidade {user_input} é de {weather}. Estão {temp} ºC. A humidade é de {humid} %. A velocidade do vento é de {wind} km/h. Para hoje, a temperatura máxima é de {maxTemp} ºC e a temperatura mínima {minTemp} ºC")
