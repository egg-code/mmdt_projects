import os
import pandas as pd
from weather_data.geonames import GeoNamesAPI
from weather_data.openweather import WeatherAPI

from dotenv import load_dotenv
from sqlalchemy import create_engine
from base import Capital_Weather, Base

def main():
    cities_df = GeoNamesAPI.get_capital_cities()
    weather_df = WeatherAPI.fetch_weather_data(cities_df)
    cities_weather_df = pd.merge(cities_df, weather_df, on='City', how='left').drop_duplicates()
    return cities_weather_df

if __name__ == '__main__':
    main()


# Loading into postgres db
load_dotenv()

user_input = input("Load data into Postgres? (Y/n): ").strip()
if user_input == 'Y':
    try:
        cities_weather_df = main()
        engine = create_engine(os.getenv('POSTGRES_URL'))
        conn = engine.connect()
        Base.metadata.create_all(engine) # create table from base.py
        cities_weather_df.to_sql('capital_weather', engine, if_exists='replace', index=False)
        print("Data loaded into Postgres")
    except Exception as er:
        print(er)
else:
    print("Wow! You are not loading data into Postgres!")
