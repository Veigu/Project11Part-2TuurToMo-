import requests

locations = {
    "Les Trois Vallées": (45.3356, 6.5890),
    "Sölden": (46.9701, 11.0078),
    "Chamonix Mont Blanc": (45.9237, 6.8694),
    "Val di Fassa": (46.4265, 11.7684),
    "Salzburger Sportwelt": (47.3642, 13.4639),
    "Alpenarena Films-Laax-Falera": (46.8315, 9.2663),
    "Kitzsteinhorn Kaprun": (47.1824, 12.6912),
    "Ski Altberg": (47.43346, 8.42053),
    "Espace Killy": (45.4481, 6.9806),
    "Špindlerův Mlýn": (50.7296, 15.6075)
}


class weerbericht:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.__weerbericht = self.get_weather_data()

    def get_weather_data(self):
        return requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.long}&appid=YOUR_API_KEY&units=metric"
        ).json()

    def get_data(self):
        response = {}
        for element in self.__weerbericht.get("list"):
            date = element.get('dt_txt').split(' ')[0]
            if date not in response:
                response.update({date: [element]})
            else:
                response.get(date).append(element)

        for dayitems in response.items():
            day = dayitems[1]

# ---------------------------------------------------------------------------------------------------------------------

            maxlist = []
            for result in day:
                maxlist.append(result.get("main").get("temp_max"))
            maxtemp = maxlist[0]
            for temp in maxlist:
                if maxtemp < temp:
                    maxtemp = temp

# ---------------------------------------------------------------------------------------------------------------------

            minlist = []
            for result in day:
                minlist.append(result.get("main").get("temp_min"))

            mintemp = minlist[0]
            for temp in minlist:
                if mintemp > temp:
                    mintemp = temp

# ---------------------------------------------------------------------------------------------------------------------

            rain = 0
            for result in day:
                if result.get("rain") is not None:
                    rain += result.get("rain").get("3h")

#---------------------------------------------------------------------------------------------------------------------

            weatherDescription = {}
            for result in day:
                description = result.get("weather")[0].get("description")
                if description in weatherDescription:
                    weatherDescription.update({description: weatherDescription.get(description) + 1})
                else:
                    weatherDescription.update({description: 1})

            windlist = []
            for result in day:
                windlist.append(result.get("wind").get("speed"))

            maxwind = windlist[0]
            for wind in windlist:
                if maxwind < wind:
                    maxwind = wind

            snow = 0
            for result in day:
                if result.get("snow") is not None:
                    snow += result.get("snow").get("3h")

            response.update({dayitems[0]: {"snow": snow, "max-temp": maxtemp, "min-temp": mintemp, "rain": rain,
                                            "wind": maxwind, "description": weatherDescription}})

        return response


# Loop through locations and retrieve data
for location, coordinates in locations.items():
    lat, long = coordinates
    weather_obj = weerbericht(lat, long)
    weather_data = weather_obj.get_data()
    print(f"Weather data for {location}: {weather_data}")
