
import requests
import json
import pandas as pd

# Setting up the API key
import os
from dotenv import load_dotenv
load_dotenv()

weather_api_key = os.getenv('weather_api_key')
username = os.getenv('geo_username')

# Getting capital cities data from geonames API
cities_url = f"http://api.geonames.org/searchJSON?q=capital&username={username}"
response = requests.get(cities_url)
cities_data = response.json()
cities_df = pd.json_normalize(cities_data['geonames'])
cities_df = cities_df[['name', 'countryName', 'population', 'lat', 'lng']]
cities_df.columns = ['City', 'Country', 'Population', 'Latitude', 'Longitude']
#print(cities_df.head()
#print(cities_df.columns)
#print(cities_df.shape)

# Getting weather data for each city from openweathermap API
weather_data = []
city_wo_data = []
for city in cities_df['City']:
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    response = requests.get(weather_url)
    w_data = response.json()
    #Seperate data of city that has data and city that doesn't have data
    if w_data['cod'] != 200:
        city_wo_data.append(city)
        continue
    weather = {
        'City': city,
        'Condition': w_data['weather'][0]['description'],
        'Min_Temperature': w_data['main']['temp_min'],
        'Max_Temperature': w_data['main']['temp_max']
    }
    weather_data.append(weather)
weather_data_df = pd.json_normalize(weather_data)

# Getting weather data for cities with lat, long
weather_data_coord = []
for city in city_wo_data:
    lat = cities_df.loc[cities_df['City'] == city, 'Latitude'].values[0]
    lon = cities_df.loc[cities_df['City'] == city, 'Longitude'].values[0]
    weather_url_coord = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"
    response_1 = requests.get(weather_url_coord).json()
    weather_coord = {
        'City':city,
        'Condition': response_1['weather'][0]['description'],
        'Min_Temperature': response_1['main']['temp_min'],
        'Max_Temperature': response_1['main']['temp_max']
    }
    weather_data_coord.append(weather_coord)
weather_data_coord_df = pd.json_normalize(weather_data_coord)

#print(weather_data_df.shape)
#print(weather_data_coord_df.shape)

# Merging the two weather dfs
weather_df = pd.concat([weather_data_df, weather_data_coord_df], axis=0)
weather_df.reset_index(drop=True, inplace=True)

# Finally merging the weather data with the cities data
cities_weather_df = pd.merge(cities_df, weather_df, on='City', how='left')

# Dropping duplicated rows
cities_weather_df = cities_weather_df.drop_duplicates(keep='first')
print(cities_weather_df.shape)
print(cities_weather_df.head())



