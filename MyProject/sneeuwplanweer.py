import requests
from sneeuwplanclass import TravelPlan

# Define the dictionary of locations with their coordinates for skiing and summer destinations
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
    "Špindlerův Mlýn": (50.7296, 15.6075),
    "Cancun": (21.1619, -86.8515),
    "Bali": (-8.4095, 115.1889),
    "Maldives": (3.2028, 73.2207),
    "Santorini": (36.3932, 25.4615),
    "Maui": (20.7984, -156.3319),
    "Seychelles": (-4.6796, 55.4915),
    "Amalfi Coast": (40.6340, 14.6027),
    "Barcelona": (41.3851, 2.1734),
    "Sydney": (-33.8688, 151.2093),
    "Rio de Janeiro": (-22.9068, -43.1729)
}


# Function to calculate temperature score
def calculate_temp_score(average_temp, desired_temp):
    temp_difference = abs(average_temp - desired_temp)
    if temp_difference <= 2:
        return 5
    elif temp_difference <= 3:
        return 4
    elif temp_difference <= 5:
        return 3
    elif temp_difference <= 7:
        return 2
    else:
        return 1


# Loop through locations and retrieve weather data
for location, coordinates in locations.items():
    lat, lon = coordinates
    travel_plan = TravelPlan(locations)
    weather_data = travel_plan.get_weather_data(lat, lon)

    # Display weather information for the location
    print(f"Weather forecast for {location}:")
    for forecast in weather_data["list"]:
        print(
            f"- Date/Time: {forecast['dt_txt']}, Temperature: {forecast['main']['temp']}°C, Rain: {forecast.get('rain', {}).get('3h', 0)}mm")
