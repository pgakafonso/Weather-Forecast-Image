import requests
from datetime import date
from datetime import timedelta


#____________DATE____________
today = date.today()

past = today + timedelta(days=-7)


#____________NEWSAPI KEY____________

api_key = 'enter here your access key' ## access newsapi API; You must register to get an access key: https://newsapi.org

city = 'Lisboa'

#__________NEWSAPI SERVICE__________

newsInfo = requests.get(
    f"https://newsapi.org/v2/everything?q={city}&language=pt&from={past}&to={today}&pageSize=5&apiKey={api_key}"
)

newsTitle1 = newsInfo.json()['articles'][0]['title']
newsLead1 = newsInfo.json()['articles'][0]['description']
newsLink1 = newsInfo.json()['articles'][0]['url']

newsTitle2 = newsInfo.json()['articles'][1]['title']
newsLead2 = newsInfo.json()['articles'][1]['description']
newsLink2 = newsInfo.json()['articles'][1]['url']

newsTitle3 = newsInfo.json()['articles'][2]['title']
newsLead3 = newsInfo.json()['articles'][2]['description']
newsLink3 = newsInfo.json()['articles'][2]['url']



print(f"As notícias mais recentes para Lisboa: \n {newsTitle1} \n {newsLead1} \n Mais informação: \n {newsLink1} \n\n")
print(f"{newsTitle2} \n {newsLead2} \n Mais informação: \n {newsLink2} \n\n")
print(f"{newsTitle3} \n {newsLead3} \n Mais informação: \n {newsLink3} \n\n")