import os
from dotenv import load_dotenv

import requests
import pandas as pd
import numpy as np


load_dotenv()


## Extracting data

def extract_covid(url: str):
    response = requests.get(url).json()
    covid_country_df = pd.DataFrame(response).T # Transpose the data
    covid_country_df.reset_index(inplace=True)
    covid_country_df.rename(columns={'index': 'country_code'}, inplace=True)
    covid_country_df = covid_country_df[["continent", "location", "total_cases", "new_cases", "total_deaths", "new_deaths", "total_cases_per_million", "total_deaths_per_million"]]
    return covid_country_df


def extract_cities(url: str):
    response = requests.get(url).json()
    raw_cities = []
    for city in response:
        raw_cities.append({
          'city': city.get('name', np.nan),
          'country_code': city.get('country_code', np.nan),
          'country_name': city.get('country_name', np.nan),
          'state' : city.get('state_name', np.nan),
          'latitude': city.get('latitude', np.nan),
          'longitude': city.get('longitude', np.nan)
        })

    cities_df = pd.DataFrame(raw_cities)
    desired_cities_df = cities_df.groupby('country_name').head(10)
    return desired_cities_df

def extract_weather_by_city(city: str):
    params = {'q':city, 'appid': os.getenv('WEATHER_API_KEY'), 'units':'metric'}
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params).json()
    return response

def extract_weather_by_coord(lat: float, lon: float):
    params = {'lat':lat, 'lon':lon, 'appid':os.getenv('WEATHER_API_KEY'), 'units':'metric'}
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params).json()
    return response

def extract_weather_data(desired_cities_df: pd.DataFrame):
    weather_data = []
    cities_wo_data = []
    desired_cities_df = desired_cities_df.to_dict(orient='records')
    for city in desired_cities_df:
        w_data = extract_weather_by_city(city['city'])
        if w_data['cod'] != 200:
            cities_wo_data.append(city)
            continue
        weather = {
            'City': city['city'],
            'Country': city['country_name'],
            'State': city['state'],
            'Latitude': city['latitude'],
            'Longitude': city['longitude'],
            'Condition': w_data['weather'][0]['description'],
            'Min_Temperature': w_data['main']['temp_min'],
            'Max_Temperature': w_data['main']['temp_max']
        }
        weather_data.append(weather)
    weather_df1 = pd.json_normalize(weather_data, max_level=1)

    weather_data_coord = []
    for city in cities_wo_data:
        lat = city['latitude']
        lon = city['longitude']
        response = extract_weather_by_coord(lat, lon)
        weather = {
            'City': city['city'],
            'Country': city['country_name'],
            'State': city['state'],
            'Latitude': city['latitude'],
            'Longitude': city['longitude'],
            'Condition': response['weather'][0]['description'],
            'Min_Temperature': response['main']['temp_min'],
            'Max_Temperature': response['main']['temp_max']
        }
        weather_data_coord.append(weather)
    
    weather_df2 = pd.json_normalize(weather_data_coord, max_level=1)
    weather_df = pd.concat([weather_df1, weather_df2], axis=0, ignore_index=True)
    return weather_df

## Transforming data
def transform_final_df(covid_df: pd.DataFrame, weather_df: pd.DataFrame):
    final_df = covid_df.merge(weather_df, how='inner', left_on='location', right_on='Country')
    final_df.drop(columns=['location'], inplace=True)
    final_df = final_df[['Country','continent', 'City', 'State', 'Latitude', 'Longitude', 'Condition', 'Min_Temperature', 'Max_Temperature', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_cases_per_million', 'total_deaths_per_million']]
    return final_df

## Loading data
def load_to_csv(final_df: pd.DataFrame, table_name: str):
    pw = os.getenv('password')
    user_input = input("Enter the password to save data to csv: ")
    if user_input == pw:
        final_df.to_csv(f"{table_name}.csv", index=False)
        print(f"{table_name} saved successfully")
    else:
        print("Wow! You just miss the chance to save the data!")