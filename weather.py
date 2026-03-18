import requests

API_KEY = "6043fa7d8fec19769c6020c70a882c45"  # paste your key here
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(location):
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    print(data)
    
    return {
        "location": location,
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

if __name__ == "__main__":
    weather = get_weather("Sydney")
    print(weather)