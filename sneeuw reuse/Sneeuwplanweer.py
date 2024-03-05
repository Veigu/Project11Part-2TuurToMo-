import json
import requests
import sneeuwplanclass

locations = {
    "Les Trois Vallées":(45.3356, 6.5890),
    "Sölden":(46.9701, 11.0078),
    "Chamonix Mont Blanc":(45.9237, 6.8694),
    "Val di Fassa":(46.4265, 11.7684),
    "Salzburger Sportwelt":(47.3642, 13.4639),
    "Alpenarena Films-Laax-Falera": (46.8315, 9.2663),
    "Kitzsteinhorn Kaprun": (47.1824, 12.6912),
    "Ski Altberg": (47.43346, 8.42053),
    "Espace Killy": (45.4481, 6.9806),
    "Špindlerův Mlýn": (50.7296, 15.6075)}




for locations, coordinates in locations.items():
    lat, long = coordinates
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid=3dceda10dca633928a81220368dd3e1e&units=metric")
    weatherdata = response.json()
    timeslots = weatherdata.get("list")
    print(f"Gemiddelde weerbericht voor {locations}")
    for x in timeslots:
        if x.get("snow") != None:
            print(x.get("snow"))




# response = requests.get("https://api.openweathermap.org/data/2.5/forecast?lat=45.3356&lon=6.5890&appid=3dceda10dca633928a81220368dd3e1e&units=metric")
# print(response)
# jsonresponse = response.json()
# print(jsonresponse)
# timeslots = jsonresponse.get("list")
# for x in timeslots:
#     # print(x.get("dt_txt"))
#     print(x.get("snow"))
#
#
# Mainclass = sneeuwplanclass.Main(69, 420)
#
# Mainclass.getWeerbericht()
# print(Mainclass.getWeerbericht())