import os
from dotenv import load_dotenv
load_dotenv()
WEATHER_API_KEY = os.getenv('weather_api_key')
GEO_USERNAME = os.getenv('geo_username')
