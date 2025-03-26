import os
import pandas as pd
import numpy as np

## Make a Class to call the functions
class E:
    def __init__(self, csv_file, parquet_file):
        self.csv_file = csv_file
        self.parquet_file = parquet_file

    def sales(self):
        df = pd.read_csv(self.csv_file)
        s_df = df[['index', 'Store_ID', 'Date', 'Weekly_Sales']]
        return s_df
    
    def extra_data(self):
        df = pd.read_parquet(self.parquet_file)
        df = df[['IsHoliday', 'CPI', 'Unemployment']]
        e_df = df.reset_index()
        return e_df

## Make a class to call transform function
class T:
    def __init__(self, sales_df, extra_data_df):
        self.sales_df = sales_df
        self.extra_data_df = extra_data_df

    def clean(self):
        df = pd.merge(self.sales_df, self.extra_data_df, on='index', how='outer')
        df['Date'] = pd.to_datetime(df['Date']) # Change df['Date'] type str to date
        # Transform 'Date' column to only 'Month'
        df['Month'] = df['Date'].dt.month

        # Fill missing values from 'IsHoliday' by validating with 'Date'
        target_dates = df.loc[df['IsHoliday'].isnull(), 'Date'].dropna().unique()
        target_dates = [date.strftime('%Y-%m-%d') for date in target_dates]
        is_business_day = np.is_busday(target_dates)
        
        # Dict to map 'Date' with 'IsHoliday'
        map_dict = {}
        for date, b_day in zip(target_dates, is_business_day):
            map_dict[str(date)] = b_day
        
        df['IsHoliday'] = df['IsHoliday'].fillna(df['Date'].astype(str).map(map_dict)).astype(bool) 
        df = df.drop(columns=['index'], axis=1)

        df.fillna({
            'CPI': df['CPI'].mean(),
            'Unemployment': df['Unemployment'].mean(),
            'Weekly_Sales': df['Weekly_Sales'].mean()}, inplace=True)
        return df

    ## Calculate average weekly sales per month
    def calculate_avg_sales(self, df):
        return df.groupby('Month').agg({'Weekly_Sales': 'mean'}).reset_index().round(3)
    
## Make a load class to save the data
class L:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    def to_csv(self, path: str):
        self.df.to_csv(path, index=False)

    def to_sqlite(self, path: str, table_name: str):
        import sqlite3
        conn = sqlite3.connect(path)
        self.df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
