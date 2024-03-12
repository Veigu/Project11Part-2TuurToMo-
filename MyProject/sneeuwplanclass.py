import requests

class TravelPlan:
    def __init__(self, locations):
        self.locations = locations

    def get_weather_data(self, lat, lon):
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=YOUR_API_KEY&units=metric"
        )
        return response.json()

