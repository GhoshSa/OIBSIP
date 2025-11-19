import requests
import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")

def get_weather(city_name):
    parameters = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  
    }

    response = requests.get(base_url, params=parameters)

    if response.status_code == 200:
        data = response.json()
        main = data["main"]
        weather = data["weather"][0]

        print(f"\nWeather in {city_name}:")
        print(f"Temperature: {main['temp']}°C")
        print(f"Humidity: {main['humidity']}%")
        print(f"Condition: {weather['description']}")
    else:
        print("City not found. Please try again.")

def main():
    print("--- Simple Weather App ---")
    city = input("Enter city name: ")
    get_weather(city)

if __name__ == "__main__":
    main()