In this project,
1. Get capital cities data from geonames api
2. Get weather data for each city from openweatherapi using city names or their coordinates
3. Get capital weather dataframe by merging cities_df and weather_df
3. Using sqlalchemy.orm, load dataframe to postgressql db

P.S. Some cities are not available to fetch data using their names so I tried to get data using their coordinates
And I've got some good experiences about fetching data from various api and packaging my scripts
Thanks to mmdt team members and Mentor Paing.

References:
https://openweathermap.org/
https://www.geonames.org/