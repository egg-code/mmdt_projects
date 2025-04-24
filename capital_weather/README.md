# 🌐 Capital Weather Data Pipeline

## Overview

This project retrieves and processes real-time weather data for capital cities around the world. It integrates data from the GeoNames and OpenWeatherMap APIs, processes the information, and stores it in a PostgreSQL database using SQLAlchemy ORM.

## Features

- 🌍 **City Data Retrieval**: Uses the GeoNames API to get details of global capital cities.
- 🌦️ **Weather Data Collection**: Fetches current weather information via the OpenWeatherMap API.
- 🔄 **Data Processing**: Merges geographic and weather datasets into a structured DataFrame.
- 🛢️ **Database Loading**: Loads processed data into a PostgreSQL database using SQLAlchemy ORM.

## How It Works

1. Fetch capital city data from GeoNames.
2. Use city coordinates to retrieve weather data from OpenWeatherMap.
3. Combine city and weather data into a single structured format.
4. Store the final data in a PostgreSQL database.

## Project Structure

capital_weather/ ├── base.py # Configuration or base logic shared across modules ├── capital_weather.py # API integration and data processing ├── main.py # Pipeline entry point: coordinates the whole process ├── weather_data/ # Output storage or intermediate data ├── requirements.txt # Python dependencies └── README.md # Project overview and documentation


## Technologies Used

- **Python 3**
- **APIs**: GeoNames, OpenWeatherMap
- **PostgreSQL**
- **SQLAlchemy ORM**
- **Pandas**

## Purpose

This project was built as part of my data engineering learning journey to demonstrate skills in:

- Integrating and consuming external APIs
- Cleaning and transforming real-world data
- Persisting data to relational databases using ORMs
- Writing modular and maintainable code

## Acknowledgments

- [GeoNames](https://www.geonames.org/) for providing public city data.
- [OpenWeatherMap](https://openweathermap.org/) for weather API services.



P.S. Some cities are not available to fetch data using their names so I tried to get data using their coordinates
And I've got some good experiences about fetching data from various api and packaging my scripts.
Thanks to mmdt team members and Mentor Paing.

