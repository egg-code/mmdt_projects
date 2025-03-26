import os
import pandas as pd
import numpy as np
from utils.etl_utils import E, T, L
import logging

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='etl_log.log'
)

logging.info('ETL Process Initializing...')
## Extract(E)
try:
    logging.info('Extracting data...')
    extract = E('./data/grocery_sales(walmart).csv', './data/extra_data.parquet')
    sales_df = extract.sales()
    extra_data_df = extract.extra_data()
    logging.info('Yay! Data extracted successfully!')
except Exception as e:
    logging.error(f"Error extracting data: {e}")

## Transform(T)
try:
    logging.info('Transforming data...')
    transform = T(sales_df, extra_data_df)
    cleaned_df = transform.clean()
    agg_sales = transform.calculate_avg_sales(cleaned_df)
    logging.info('Gotcha! Data transformed successfully!')
except Exception as e:
    logging.error(f"Error transforming data: {e}")

## Load(L)
try:
    logging.info('Loading data...')
    load_df = L(cleaned_df)
    load_agg_sales = L(agg_sales)

    load_df.to_csv('./data/cleaned_walmart_sales.csv')
    load_df.to_sqlite('./data/cleaned_walmart_sales.db', 'cleaned_walmart_sales')

    load_agg_sales.to_csv('./data/avg_monthly_sales.csv')
    load_agg_sales.to_sqlite('./data/avg_monthly_sales.db', 'avg_monthly_sales')
    logging.info('Yahoo! Data loaded successfully!')
except Exception as e:
    logging.error(f"Error loading data: {e}")

## Validate
try:
    logging.info('Validating data...')
    
    read_csv = pd.read_csv('./data/cleaned_walmart_sales.csv')
    assert read_csv == cleaned_df, f'Data mismatch in CSV file: {read_csv.compare(cleaned_df)}'
    logging.info('CSV file validated successfully!')
    
    conn = sqlite3.connect('./data/cleaned_walmart_sales.db')
    read_sqlite = pd.read_sql('SELECT * FROM cleaned_walmart_sales', conn)
    conn.close()
    assert read_sqlite.equals(cleaned_df), 'Data mismatch in sqlite db'
    logging.info('SQLite db validated successfully!')

except Exception as e:
    logging.error(f"Error validating data: {e}")

logging.info('ETL Process Completed!')

print('ETL Process Completed!')

