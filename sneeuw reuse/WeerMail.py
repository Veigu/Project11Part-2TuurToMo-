import Sendmail
import weerbericht
import requests
import json
import datetime

#vraag voor mail:
# adress = input("mailadres: ")

#het weerbericht
weer = weerbericht.weerbericht()
result = weer.getData()
resultlist = list(result.values())
descriptionList = list(resultlist[0].get('description').keys())
print(result)

#Zorgt er voor dat de text die gestuurd word overzichtelijker is met commas en "and"
descriptionText = ""
for element in descriptionList[:2]:
    descriptionText += element + ", "
if len(descriptionList) >= 2:
    descriptionText += descriptionList[-2] + " and "

descriptionText += descriptionList[-1]


locations = {
    "1lat": 45.3356,
    "1lon": 6.5890,
    "2lat": 46.9701,
    "2lon": 11.0078,
    "3lat": 45.9237,
    "3lon": 6.8694,
    "4lat": 46.4265,
    "4lon": 11.7684,
    "5lat": 47.3642,
    "5lon": 13.4639,
    "6lat": 46.8315,
    "6lon": 9.2663,
    "7lat": 47.1824,
    "7lon": 12.6912,
    "8lat": 47.43346,
    "8lon": 8.42053,
    "9lat": 45.4481,
    "9lon": 6.9806,
    "10lat": 50.7296,
    "10lon": 15.6075
}

print("""
locations:
1. Les Trois Vallées
2. Sölden
3. Chamonix-Mont Blanc
4. Val di Fassa
5. Salzburger Sportwelt
6. Alpenarena Flims-Laax-Falera
7. Kitzsteinhorn Kaprun
8. Ski Arlberg
9. Espace Killy
10. Spindleruv Mlyn
""")

chosenloc = input("Give me the number of the location you want: ")

response = requests.get(
    f"https://api.openweathermap.org/data/2.5/forecast?lat={locations[chosenloc + "lat"]}&lon={locations[chosenloc + "lon"]}&appid=3dceda10dca633928a81220368dd3e1e&units=metric"
)

#de inhoud van de mail:
mail = f'''
Todays weather report: \n 
The temperatures are in between {resultlist[0].get("min-temp")}°C and {resultlist[0].get("max-temp")}°C.
There will be {resultlist[0].get("snow")} mm snow

'''
#mail sturen
# Sendmail.main(adress, mail)
