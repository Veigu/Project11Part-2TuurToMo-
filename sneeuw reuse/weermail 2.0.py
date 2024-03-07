import requests
import weerbericht2

# Define the dictionary of locations with their coordinates
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

# Display the list of locations for the user to choose from
print("Locations:")
for index, location in enumerate(locations.keys(), start=1):
    print(f"{index}. {location}")

# Ask the user for the number of the location they want
chosenloc = input("Give me the number of the location you want: ")

# Retrieve the coordinates of the chosen location
chosen_location = list(locations.values())[int(chosenloc) - 1]
lat, lon = chosen_location

# get weather data for the chosen location
response = requests.get(
    f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=YOUR_API_KEY&units=metric"
)
weatherdata = response.json()

# Get timeslots if available
timeslots = weatherdata.get("list")

# Display weather information for the chosen location
print(f"Weather forecast for {list(locations.keys())[int(chosenloc) - 1]}:")
if timeslots is not None:
    for weerbericht2 in timeslots:
        if "snow" in weerbericht2:
            if weerbericht2.get("snow"):
                print(weerbericht2.get(snow))
else:
    print(f"No weather data available for this location.", {snow})
