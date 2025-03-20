import requests
import pandas as pd
from weather_data.config import GEO_USERNAME

# Class to get capital cities data from geonames API
class GeoNamesAPI:
    BASE_URL = "http://api.geonames.org/searchJSON"
    
    @staticmethod
    def get_capital_cities():
        params = {"q": "capital", "username": GEO_USERNAME}
        response = requests.get(GeoNamesAPI.BASE_URL, params=params)
        data = response.json()
        df = pd.json_normalize(data['geonames'])
        df = df[['name', 'countryName', 'population', 'lat', 'lng']]
        df.columns = ['City', 'Country', 'Population', 'Latitude', 'Longitude']
        return df