import requests

class weerbericht:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.__weather_data = self.get_weather_data()

    def get_weather_data(self):
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}&appid=5fb6f2559f1424191995a7eebc27f0c2&units=metric"
        )
        return response.json()

    def get_data(self):
        response = {}
        for element in self.__weather_data.get("list"):
            date = element.get('dt_txt').split(' ')[0]
            if date not in response:
                response.update({date: [element]})
            else:
                response.get(date).append(element)

        for dayitems in response.items():
            day = dayitems[1]

            # Calculate average temperature for the day
            temperatures = [result.get("main").get("temp") for result in day]
            average_temp = sum(temperatures) / len(temperatures)

            # Calculate total rainfall for the day
            total_rain = sum(result.get("rain", {}).get("3h", 0) for result in day)

            response.update({dayitems[0]: {"average_temp": average_temp, "rain": total_rain}})

        return response
