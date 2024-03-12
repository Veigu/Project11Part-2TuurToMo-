# Import necessary modules and classes from Part 1
from MyProject.SummerSun import calculate_rain_score
from MyProject.sneeuwplanweer import calculate_temp_score
from weerbericht import weerbericht

# Define the dictionary of summer destinations with their coordinates
summer_destinations = {
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

# Display the list of summer destinations for the user to choose from
print("Summer Destinations:")
for index, destination in enumerate(summer_destinations.keys(), start=1):
    print(f"{index}. {destination}")

# Ask the user for the number of the destination they want
chosen_dest = input("Enter the number of your desired destination: ")

# Retrieve the coordinates of the chosen destination
chosen_destination = list(summer_destinations.values())[int(chosen_dest) - 1]
lat, lon = chosen_destination

# Ask the user for their ideal temperature and rain tolerance
ideal_temp = float(input("Enter your ideal temperature (in Celsius): "))
rain_tolerance = input("Choose your rain tolerance ('very little', 'less than average', or 'no preference'): ")

# Get weather data for the chosen destination
weather_obj = weerbericht(lat, lon)
weather_data = weather_obj.get_data()

# Calculate scores for each destination based on temperature and rain tolerance
scores = {}
for destination, data in weather_data.items():
    temp_score = calculate_temp_score(data['average_temp'], ideal_temp)
    rain_score = calculate_rain_score(data['rain'], rain_tolerance)
    total_score = temp_score + rain_score
    scores[destination] = total_score

# Rank the destinations based on their scores
ranked_destinations = sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Display the ranking and weather information for the destinations
print("Ranking of Summer Destinations:")
for i, (destination, score) in enumerate(ranked_destinations, start=1):
    print(f"{i}. {destination}:")
    print(f"   - Average Temperature: {weather_data[destination]['average_temp']}°C")
    print(f"   - Rainfall: {weather_data[destination]['rain']} mm")
