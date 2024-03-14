import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# List of summer destinations with their latitude and longitude
destinations = {
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

# Define Google API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_weather_forecast(api_key, latitude, longitude):
    # Function to fetch weather forecast from OpenWeatherMap API
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data["list"][:5]  # only first 5 days


def format_weather_forecast(weather_forecast):
    # Function to format weather forecast data
    forecasts = []
    for forecast in weather_forecast:
        date = forecast["dt_txt"].split()[0]
        temperature = forecast["main"]["temp"]
        description = forecast["weather"][0]["description"]
        wind_speed = forecast["wind"]["speed"]
        precipitation = forecast["rain"]["3h"] if "rain" in forecast else 0

        # Append formatted forecast to forecasts list
        forecasts.append(
            f"Date: {date}\nTemperature: {temperature}°C\nDescription: {description}\nWind Speed: {wind_speed} m/s\nPrecipitation: {precipitation} mm")

    return "\n\n".join(forecasts)


def main():
    # Main function
    # Fetch API key and google credentials
    openweathermap_api_key = os.getenv("WEATHER_TOKEN")
    google_credentials_file = "credentials.json"

    # Fetching weather forecast for each destination
    forecasts_text = ""
    for destination, (latitude, longitude) in destinations.items():
        # Fetch current destination
        weather_forecast = get_weather_forecast(openweathermap_api_key, latitude, longitude)
        destination_forecast_text = f"{destination} Forecast:\n\n{format_weather_forecast(weather_forecast)}\n\n"
        forecasts_text += destination_forecast_text

    # Sending email
    receiver_email = input("Enter your email address: ")
    send_email(google_credentials_file, receiver_email, forecasts_text)


def send_email(credentials_file, receiver_email, message):
    # Function to send email using Gmail API
    # Initialize credentials as None
    creds = None
    # Check if token file exists
    if not os.path.exists("token.json"):
        pass
    else:
        # Load Google credentials from token file
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the credentials
            creds.refresh(requests.Request())
        else:
            # Authenticate user and generate credentials
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Write updated credentials to token file
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Build Gmail service
        service = build("gmail", "v1", credentials=creds)

        # Create a plain text message
        msg = MIMEMultipart()
        msg['to'] = receiver_email
        msg['subject'] = "Weather Forecast for Summer Destinations"

        # Attach the plain text message
        msg.attach(MIMEText(message, 'plain'))

        # Encode the message as base64
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        # Send the email
        service.users().messages().send(userId="me", body={'raw': raw_message}).execute()

        print("Email sent successfully!")

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
