import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests

# Google API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

# Function to send email using API
def send_email(receiver_email, mail_content):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("gmail", "v1", credentials=creds)

        message = EmailMessage()
        message.set_content(mail_content)
        message["To"] = receiver_email
        message["From"] = "moe.ramault@gmail.com"
        message["Subject"] = "Summer Weather Forecast"
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"message": {"raw": encoded_message}}
        draft = service.users().drafts().create(userId="me", body=create_message).execute()
        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
        service.users().drafts().send(userId="me", body=draft).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")

# Retrieve weather data and send email
def main():
    # Ask for recipient's email address
    receiver_email = input("Enter recipient's email address: ")
    while not receiver_email:
        print("Please enter a valid email address.")
        receiver_email = input("Enter recipient's email address: ")

    # Define summer destinations
    global weather_data
    destinations = {
        "Ankara, Turkije": (39.9334, 32.8597),
        "Athene, Griekenland": (37.9838, 23.7275),
        "La Valette, Malta": (35.8989, 14.5146),
        "Sardinië, Italië": (40.1209, 9.0129),
        "Sicilië, Italië": (37.5994, 14.0154),
        "Nicosia, Cyprus": (35.1856, 33.3823),
        "Mallorca, Spanje": (39.6953, 3.0176),
        "Lagos, Portugal": (37.1022, -8.6739),
        "Mauritius": (-20.3484, 57.5522),
        "Boekarest, Roemenië": (44.4268, 26.1025)
    }

    # Ask user for preferred temperature
    preferred_temp = float(input("Enter your preferred temperature (in Celsius): "))

    # Ask user for rain tolerance
    rain_tolerance = input("Enter your rain tolerance (Zeer weinig/Minder dan 2mm/Geen voorkeur): ")
    while rain_tolerance.lower() not in ["zeer weinig", "minder dan 2mm", "geen voorkeur"]:
        print("Invalid input. Please enter 'Zeer weinig', 'Minder dan 2mm', or 'Geen voorkeur'.")
        rain_tolerance = input("Enter your rain tolerance (Zeer weinig/Minder dan 2mm/Geen voorkeur): ")

    # Retrieve weather data for each destination
    destination_scores = {}
    for destination, coordinates in destinations.items():
        lat, lon = coordinates
        weather_data = get_weather_data(lat, lon)
        score = calculate_score(weather_data["main"]["temp"], weather_data["rain"]["1h"], preferred_temp, rain_tolerance)
        destination_scores[destination] = score

    # Sort destinations by score
    sorted_destinations = sorted(destination_scores.items(), key=lambda x: x[1], reverse=True)

    # Create email content
    email_content = "Summer Weather Forecast for Top 10 Destinations:\n\n"
    for i, (destination, score) in enumerate(sorted_destinations[:10], 1):
        email_content += f"{i}. {destination}\n"
        email_content += f"   Average Temperature: {weather_data['main']['temp']}°C\n"
        if weather_data["rain"]["1h"] < 1:
            rain_forecast = "Zeer weinig"
        elif weather_data["rain"]["1h"] < 2:
            rain_forecast = "Minder dan 2mm"
        else:
            rain_forecast = "Veel"
        email_content += f"   Rain Forecast: {rain_forecast}\n\n"

    # Send email to recipient
    send_email(receiver_email, email_content)

# Retrieve weather data from OpenWeatherMap API
def get_weather_data(latitude, longitude):
    api_key = "5fb6f2559f1424191995a7eebc27f0c2"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    weather_data = {
        "main": {
            "temp": data.get("main", {}).get("temp")
        },
        "rain": {
            "1h": data.get("rain", {}).get("1h", 0)
        }
    }

    return weather_data

# Function to calculate score based on temperature and rain tolerance
def calculate_score(temperature, rain, preferred_temp, rain_tolerance):
    temp_range = abs(temperature - preferred_temp)
    if temp_range <= 2:
        temp_score = 5
    elif temp_range <= 3:
        temp_score = 4
    elif temp_range <= 5:
        temp_score = 3
    elif temp_range <= 7:
        temp_score = 2
    else:
        temp_score = 1

    if rain_tolerance.lower() == "zeer weinig" and rain < 1:
        rain_score = 4
    elif rain_tolerance.lower() == "minder dan 2mm" and rain < 2:
        rain_score = 4
    else:
        rain_score = 0

    return temp_score + rain_score

if __name__ == "__main__":
    main()
