import requests
import pandas as pd
from weather_data.config import WEATHER_API_KEY

class WeatherAPI:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def get_weather_by_city(city):
        params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
        response = requests.get(WeatherAPI.BASE_URL, params=params)
        return response.json()
    
    @staticmethod
    def get_weather_by_coordinates(lat, lon):
        params = {"lat": lat, "lon": lon, "appid": WEATHER_API_KEY, "units": "metric"}
        response = requests.get(WeatherAPI.BASE_URL, params=params)
        return response.json()
    
    @staticmethod
    def fetch_weather_data(cities_df):
        weather_data, city_wo_data = [], []
        
        for city in cities_df['City']:
            w_data = WeatherAPI.get_weather_by_city(city)
            if w_data['cod'] != 200:
                city_wo_data.append(city)
                continue
            weather_data.append({
                'City': city,
                'Condition': w_data['weather'][0]['description'],
                'Min_Temperature': w_data['main']['temp_min'],
                'Max_Temperature': w_data['main']['temp_max']
            })
        
        weather_data_df = pd.json_normalize(weather_data)
        
        weather_data_coord = []
        
        for city in city_wo_data:
            lat = cities_df.loc[cities_df['City'] == city, 'Latitude'].values[0]
            lon = cities_df.loc[cities_df['City'] == city, 'Longitude'].values[0]
            response = WeatherAPI.get_weather_by_coordinates(lat, lon)
            weather_data_coord.append({
                'City': city,
                'Condition': response['weather'][0]['description'],
                'Min_Temperature': response['main']['temp_min'],
                'Max_Temperature': response['main']['temp_max']
            })
        
        weather_data_coord_df = pd.json_normalize(weather_data_coord)
        return pd.concat([weather_data_df, weather_data_coord_df], axis=0, ignore_index=True)