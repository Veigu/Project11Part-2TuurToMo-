import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests

# scopes for Gmail API
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.compose"]

# Function to calculate score
def calculate_score(temperature, snowfall):
    if temperature < 0:
        score = 5
    elif 0 <= temperature < 5:
        score = 4
    elif 5 <= temperature < 10:
        score = 3
    else:
        score = 1

    if snowfall > 5:
        score = min(score + 1, 5)

    return score

# Function to send email using API
def send_email(mailadres, mail):
    creds = None
    # token.json stores the user's data
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
        message.set_content(mail)
        # my email:
        message["To"] = "moe.ramault@gmail.com"
        # recieving email:
        message["From"] = mailadres
        # onderwerp in mailcredentials.json
        message["Subject"] = "Weerbericht"
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"message": {"raw": encoded_message}}
        draft = service.users().drafts().create(userId="me", body=create_message).execute()
        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
        service.users().drafts().send(userId="me", body=draft).execute()
    # if there is a error tell this to the client and skip code
    except HttpError as error:
        print(f"An error occurred: {error}")

# Retrieve snowfall data and send email
def main():
    # Ask for recipient's email address
    receiver_email = input("Enter recipient's email address: ")
    while not receiver_email:
        print("Please enter a valid email address.")
        receiver_email = input("Enter recipient's email address: ")

    # Define your locations
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

    # Retrieve snowfall data
    snowfall_data = get_snowfall_data(locations)

    # Make email with snowfall data
    email_info = "Snowfall Forecast for the Next 5 Days:\n"
    for location, data in snowfall_data.items():
        email_info += f"Location: {location}\n"
        for day, snowfall in data.items():
            email_info += f"{day}: {snowfall} mm\n"
        email_info += "\n"

    # Send email to recipient
    send_email(receiver_email, email_info)

# Retrieve snowfall data for next 5 days
def get_snowfall_data(locations):
    snowfall_data = {}
    for location, coordinates in locations.items():
        lat, lon = coordinates
        # Retrieving snowfall data
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=3dceda10dca633928a81220368dd3e1e&units=metric")
        weatherdata = response.json()
        timeslots = weatherdata.get("list")
        snowfall_data[location] = {}
        for x in timeslots:
            if x.get("snow") is not None:
                snowfall_data[location][x["dt_txt"]] = x.get("snow").get("3h")
    return snowfall_data

if __name__ == "__main__":
    main()
