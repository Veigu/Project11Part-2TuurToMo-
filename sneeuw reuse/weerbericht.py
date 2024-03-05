import Sneeuwplanweer
import requests

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


class weerbericht:
    def __init__(self):
        self.__weerbericht = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid=3dceda10dca633928a81220368dd3e1e&units=metric").json()


    def getData(self):
        response = {}
        for element in self.__weerbericht.get("list"):
            date = element.get('dt_txt').split(' ')[0]
            if date not in response:
                response.update({date: [element]})
            else:
                response.get(date).append(element)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# zoek en get de max temp van alle timeslots van een dag
        for dayitems in response.items():
            day = dayitems[1]
            maxlist =  []
            for result in day:
                maxlist.append(result.get("main").get("temp_max"))
            maxtemp = maxlist[0]
            for temp in maxlist:
                if maxtemp < temp:
                    maxtemp = temp

 #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#zoek en get de minimum temp van alle timeslots van een dag
            minlist = []
            for result in day:
                minlist.append(result.get("main").get("temp_min"))

            mintemp = minlist[0]
            for temp in minlist:
                if mintemp > temp:
                    mintemp = temp

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#zoek en get de regen
            rain = 0
            for result in day:
                if result.get("rain") is not None:
                    rain += result.get("rain").get("3h")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#zoek en get het weer
            weatherDescription = {}
            for result in day:
                description = result.get("weather")[0].get("description")
                if description in weatherDescription:
                    weatherDescription.update({description: weatherDescription.get(description) +1})
                else:
                    weatherDescription.update({description : 1})

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#zoek en get de wind en speed
            windlist = []
            for result in day:
                windlist.append(result.get("wind").get("speed"))

            maxwind = windlist[0]
            for wind in windlist:
                if maxwind < wind:
                    maxwind = wind

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#zoek en get de sneeuw

            total_snow = 0
            snowlist = []
            for result in day:
                snowlist.append(result.get("snow"))

            total_snow = sum(snowlist)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


            #update de data die we net hebben gezocht en get
            response.update({dayitems[0]: {"max-temp": maxtemp, "min-temp": mintemp, "rain" : rain, "wind" :maxwind, "description": weatherDescription, "snow": total_snow}})

        return response
