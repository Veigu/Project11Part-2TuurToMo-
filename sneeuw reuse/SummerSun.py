# Modify the weerbericht class to include functionality for summer destinations
from google.auth.transport import requests


class weerbericht:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.__weerbericht = self.get_weather_data()

    def get_weather_data(self):
        # Modify the API request to use the provided API key and fetch summer weather data
        return requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.long}&appid=YOUR_API_KEY&units=metric"
        ).json()

    def get_data(self):
        # Modify the data processing logic to include summer weather parameters
        response = {}
        for element in self.__weerbericht.get("list"):
            date = element.get('dt_txt').split(' ')[0]
            if date not in response:
                response.update({date: [element]})
            else:
                response.get(date).append(element)

        for dayitems in response.items():
            day = dayitems[1]

            maxlist = []
            for result in day:
                maxlist.append(result.get("main").get("temp_max"))
            maxtemp = maxlist[0]
            for temp in maxlist:
                if maxtemp < temp:
                    maxtemp = temp

            minlist = []
            for result in day:
                minlist.append(result.get("main").get("temp_min"))

            mintemp = minlist[0]
            for temp in minlist:
                if mintemp > temp:
                    mintemp = temp

            rain = 0
            for result in day:
                if result.get("rain") is not None:
                    rain += result.get("rain").get("3h")

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

            # Update the response dictionary to include summer weather parameters
            response.update({dayitems[0]: {"snow": snow, "max-temp": maxtemp, "min-temp": mintemp, "rain": rain,
                                            "wind": maxwind, "description": weatherDescription}})

        return response

# Create a new function or class to calculate hidden scores for summer destinations
def calculate_hidden_scores(weather_data, ideal_temp, rain_tolerance):
    scores = {}
    for location, data in weather_data.items():
        # Calculate temperature score
        temp_score = calculate_temperature_score(data["max-temp"], ideal_temp)
        # Calculate rain score
        rain_score = calculate_rain_score(data["rain"], rain_tolerance)
        # Calculate total hidden score
        total_score = temp_score + rain_score
        # Store the total score for the location
        scores[location] = total_score
    return scores

def calculate_temperature_score(actual_temp, ideal_temp):
    # Calculate temperature score based on the difference between actual and ideal temperature
    temp_difference = abs(actual_temp - ideal_temp)
    if temp_difference <= 2:
        return 5
    elif temp_difference <= 3:
        return 4
    elif temp_difference <= 5:
        return 3
    elif temp_difference <= 7:
        return 2
    elif temp_difference <= 10:
        return 1
    else:
        return 0

def calculate_rain_score(actual_rain, rain_tolerance):
    # Calculate rain score based on the rain tolerance
    if rain_tolerance == "zeer weinig":
        if actual_rain < 1:
            return 4
    elif rain_tolerance == "minder dan 2mm":
        if actual_rain < 2:
            return 4
    else:
        return 4
    return 0

# Modify the email sending function to include ranking of destinations based on hidden scores
def send_email_summer(destinations, hidden_scores):
    # Sort destinations based on hidden scores
    ranked_destinations = sorted(destinations.keys(), key=lambda x: hidden_scores[x], reverse=True)

    # Compose email content
    email_content = "Ranking of Summer Destinations:\n"
    for index, destination in enumerate(ranked_destinations, start=1):
        email_content += f"{index}. {destination}:\n"
        # Include weather information for the destination
        weather_info = destinations[destination]
        email_content += f"   - Average Temperature: {weather_info['max-temp']}°C\n"
        if weather_info["rain"] < 1:
            rain_forecast = "zeer weinig (<1mm)"
        elif weather_info["rain"] < 2:
            rain_forecast = "minder dan 2mm"
        else:
            rain_forecast = "veel"
        email_content += f"   - Rain Forecast: {rain_forecast}\n\n"

    # Send email to user
    # Implement email sending logic here

# Main function to handle user interaction
def main():
    print("Welcome to Summer Sun! Please select your preferences:")
    ideal_temp = float(input("Enter your ideal temperature (in °C): "))
    rain_tolerance = input("Enter your rain tolerance (zeer weinig/minder dan 2mm/geen voorkeur): ")

    # Retrieve weather data for summer destinations
    weather_data = {}
    for location, coordinates in locations.items():
        lat, lon = coordinates
        weather_obj = weerbericht(lat, lon)
        weather_data[location] = weather_obj.get_data()

    # Calculate hidden scores for destinations
    hidden_scores = calculate_hidden_scores(weather_data, ideal_temp, rain_tolerance)

    # Send email with ranked destinations
    send_email_summer(weather_data, hidden_scores)

if __name__ == "__main__":
    main()
