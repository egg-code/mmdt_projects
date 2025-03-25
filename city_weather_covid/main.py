import os
import pandas as pd
from utils.etl_utils import extract_covid, extract_cities, extract_weather_data, transform_final_df, load_to_csv

covid_url = "https://raw.githubusercontent.com/owid/covid-19-data/refs/heads/master/public/data/latest/owid-covid-latest.json"
cities_url = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/refs/heads/master/json/cities.json"

# Extracting data
def main():
    covid_df = extract_covid(covid_url)
    cities_df = extract_cities(cities_url)
    weather_df = extract_weather_data(cities_df)
    final_df = transform_final_df(covid_df, weather_df)
    print(final_df.head())
    print(final_df.tail())
    print(final_df.columns)
    print(final_df.info())
    load_to_csv(final_df, 'City_Weather_Covid_Data.csv')

if __name__ == '__main__':
    main()


