import json
import random
from datetime import datetime
from swarm import Agent

# dummy data of weather
weather_data = {
    "Tokyo": {"temp_range": (10, 30), "conditions": ["sunny", "cloudy", "rainy", "snowy"]},
    "Osaka": {"temp_range": (15, 25), "conditions": ["sunny", "cloudy", "rainy", "snowy"]},
    "Fukuoka": {"temp_range": (12, 28), "conditions": ["sunny", "cloudy", "rainy", "snowy"]},
}

def get_weather(location: str, time="now"):
    """get the current weather in a given location. Location MUST be a city name."""
    if location not in weather_data:
        return json.dumps({"error": f"Location {location} not found in weather data."})

    city_data = weather_data[location]
    temperature = random.randint(*city_data["temp_range"])
    condition = random.choice(city_data["conditions"])

    current_time = datetime.now().strftime("%H:%M")

    weather_info = {
        "location": location,
        "temperature": f"{temperature}°C",
        "condition": condition,
        "time": current_time,
    }

    return json.dumps(weather_info)

def send_email(recipient, subject, body):
    """function to send an email"""
    print("Sending email...")
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    return "Sent!"

weather_agent = Agent(
    name="Weather Agent",
    instructions="""
    You are a helpful weather information agent.
    When a user asks about a city, please provide weather information for that city.
    You can also send weather information by email if the user requests it.
    Currently, you can provide weather information for Tokyo, Osaka, and Fukuoka.
    """,
    functions=[get_weather, send_email],
)
