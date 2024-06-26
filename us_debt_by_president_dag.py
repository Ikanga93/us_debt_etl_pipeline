# Import necessary modules

import sys
import os
import logging
import logging.handlers
import requests
import pendulum
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import timedelta

# Add the directory containing my modules to the python path
sys.path.append('/Users/jbshome/Desktop/us_debt_etl_pipeline')

from president_data import year_to_president

'''
My logs are being printed in the console instead of to the file. 
To ensure that logging is directed to the file, so I need to set up logging handlers.
'''
# Define the log directory and file path
log_dir = '/Users/jbshome/Desktop/us_debt_etl_pipeline/logs'
log_file = 'us_debt_by_president.log'

# Check the log directory exists
os.makedirs(log_dir, exist_ok=True)

# Check directory permissions
if not os.access(log_dir, os.W_OK):
    raise PermissionError(f'You do not have write permissions to {log_dir}')

# Clear existing log handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Logging configuration
logging.basicConfig(filename='/Users/jbshome/Desktop/us_debt/logs/us_debt_by_president.log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create file handler
file_handler = logging.FileHandler(os.path.join(log_dir, log_file))
file_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logging.getLogger().addHandler(file_handler)
logging.getLogger().addHandler(console_handler)

# Url to fetch the data
url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_outstanding?fields=record_fiscal_year, debt_outstanding_amt&sort=-record_fiscal_year&format=json&page[number]=1&page[size]=235'
# Path to csv file
us_debt_csv = '/Users/jbshome/Desktop/us_debt_etl_pipeline/csv_files/us_debt_by_president.csv'

#Function to extract the data
def extract_task(api_url):
    try: 
        # Get the data from the api
        r = requests.get(api_url)
        json_data = r.json()

        # Extract the data from the json object
        if 'data' not in json_data:
            logging.error('No data found in json object')
            return None
        data = json_data['data']

        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        logging.info('Data extracted successfully')
        return df
    except Exception as e:
        logging.error(f'Error extracting data: {str(e)}')
        return None

# Call the extract function
df = extract_task(url)

# Function to transform the data
def transform_task(data):
# Transform the data
    try:
    # Adding a new column to the DataFrame from another python file
        if data is not None:
            # Add the president column to the DataFrame
            data['president'] = data['record_fiscal_year'].astype(int).map(year_to_president)
            logging.info('President column added to DataFrame')
        
        else:
            logging.error('Could not add president column to DataFrame')

        # Change the president data to title case
        data['president'] = data['president'].str.title()

        # Also I need to conver the record_fiscal_year and debt_outstanding_amt to appropriate data types
        # Convert the record_fiscal_year to int
        data['record_fiscal_year'] = data['record_fiscal_year'].astype(int)
        # Remove the commas from the debt_outstanding_amt and convert it to float
        data['debt_outstanding_amt'] = data['debt_outstanding_amt'].astype(float)

        # I thought it will be great if I create more columns to make the data more informative
        # Create a new column to show the debt in trillions
        # data['debt_outstanding_trillions'] = data['debt_outstanding_amt'] / 1e12
        # Create a new column to show the debt in billions
        # data['debt_outstanding_billions'] = data['debt_outstanding_amt'] / 1e9
        # Create a new column to show the debt in millions
        # data['debt_outstanding_millions'] = data['debt_outstanding_amt'] / 1e6
        # Round the debt_outstanding_trillions and debt_outstanding_billions columns to 2 decimal places
        # data['debt_outstanding_trillions'] = data['debt_outstanding_trillions'].round(2)
        # data['debt_outstanding_billions'] = data['debt_outstanding_billions'].round(2)
        # data['debt_outstanding_millions'] = data['debt_outstanding_millions'].round(2)
        # Calculate the debt per president
        # data['debt_per_president'] = data.groupby('president')['debt_outstanding_trillions'].diff().fillna(0)
        # Calculate the debt increase per year
        # data['debt_increase_per_year'] = data.groupby('president')['debt_outstanding_trillions'].diff().fillna(0) / 4
        # Calculate the debt increase per day
        # data['debt_increase_per_day'] = data.groupby('president')['debt_outstanding_trillions'].diff().fillna(0) / 365
        # Calculate the debt increase per hour
        # data['debt_increase_per_hour'] = data.groupby('president')['debt_outstanding_trillions'].diff().fillna(0) / 8760
        # Need to sort the data by record_fiscal_year in ascending order
        # data = data.sort_values('record_fiscal_year', ascending=True)
        # Calculate how much each president added to the debt without repeating the president's name
        # data['debt_added'] = data.groupby('president')['debt_outstanding_trillions'].diff().fillna(0)
        # Geting the total debt added by each president
        # data['total_debt_added'] = data.groupby('president')['debt_added'].cumsum()
        # Create a new column to show the change in debt in percentage form for each president using lambda function
        # data['debt_change_percentage'] = data.groupby('president')['debt_outstanding_amt'].pct_change().fillna(0)
        # Need to have only one name for each president
        # data['president'] = data['president'].drop_duplicates()
        # data['debt_change_percentage'] = data.groupby('president')['debt_change_percentage'].transform(lambda x: x.fillna(x.mean()))
        # Want to show all data
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        # Reset the index
        # Add all duplicated president names in one, add their debts in one row, and combine the years in one row as a range
        #data = data.groupby('president').agg({'record_fiscal_year': lambda x: f'{x.min()} - {x.max()}', 'debt_outstanding_amt': 'sum'}).reset_index()
        # Sort the data by record_fiscal_year in ascending order
        # data = data.sort_values('record_fiscal_year', ascending=True, ignore_index=True)
        # Calculate the debt added by each president on top of the previous year per president
        # Create a new column that calculate the increase per year for each persident compare to the previous year and 
        # add a dollar sign to it and still keep it as an integer



        # Create a new column that calculate the increase per year for each persident compare to the previous year. Add a dollar sign to the new column and still keep it as an integer
        # data['debt_added'] = data.groupby('president')['debt_outstanding_amt'].diff().fillna(0)
        # Add the dollar sign to the debt_added column and still keep it as an integer
        # data['debt_added'] = data['debt_added'].apply(lambda x: f'${int(x):,}' if x > 0 else f'-${int(x):,}')

        # Add all duplicated president names in one, add their debts in one row as a range and a whole number with a dollar sign, and combine the years in one row as a range
        # data = data.groupby('president').agg({'record_fiscal_year': lambda x: f'{x.min()} - {x.max()}'}).reset_index()
        # Add a dollar sign to the debt_outstanding_amt column and still keep it as integer

        # Add all duplicated president names in one, add their debts in one row, combine the years in one row as a range and create a new column that calculate the increase per year for each persident compare to the previous year
        # data = data.groupby('president').agg({'record_fiscal_year': lambda x: f'{x.min()} - {x.max()}', 'debt_outstanding_amt': 'sum', 'debt_added': 'sum'}).reset_index()
        # Add a new coclumn that combine in range the total_debt per president
        # data['debt_outstanding_amt'] = data['debt_outstanding_amt'].apply(lambda x: f'${int(x):,}')
        # Sort the data by record_fiscal_year in ascending order
        data = data.sort_values('record_fiscal_year', ascending=True, ignore_index=True)
        # Show the debt_added column in whole numbers and add the dollar sign to it and still keep it as an integer and the negative sign if the debt is reduced should be before the dollar sign
        # data['debt_added'] = data['debt_added'].apply(lambda x: f'${int(x):,}' if x > 0 else f'-${int(x):,}')
        # Show the debt_outstanding_amt column in whole numbers and add the dollar sign to it and still keep it as an integer
        # data['debt_outstanding_amt'] = data['debt_outstanding_amt'].apply(lambda x: f'${int(x):,}')
        # Show the debt_added column in whole numbers
        # data['debt_added'] = data['debt_added'].apply(lambda x: f'{int(x):,}')
        # Change the column names of the debt_added and debt_outstanding_amt columns
        data = data.rename(columns={'debt_outstanding_amt': 'total_debt', 'debt_added': 'debt_added_per_president'})
        # Change the column of fiscal year to years_in_office and president to president_name
        data = data.rename(columns={'record_fiscal_year': 'period_in_office', 'president': 'president_name'})
        # Add a new column to show the number of years each president spent in office
        # data['years_in_office'] = data['period_in_office'].apply(lambda x: int(x.split('-')[1]) - int(x.split('-')[0]) + 1)
     
        # Remove the total_debt column
        # data = data.drop(columns='total_debt')
        # Add a new coclumn that combine in range the total_debt per president
        # data['total_debt'] = data['total_debt'].apply(lambda x: f'${int(x):,}')

        logging.info('Data transformed successfully')
        return data
    except Exception as e:
        logging.error(f'Error transforming data: {str(e)}')
        return None

# Call the transform function
cleaned_df = transform_task(df)

# Function to load the data
def load_task(df, csv_file):
    # Save to csv
    try:
        df.to_csv(csv_file, index=False)
        logging.info('Data saved to csv successfully')
        return df
    except Exception as e:
        logging.error(f'Error saving data to csv: {str(e)}')
        return None

# Call the load_task function
print(load_task(cleaned_df, us_debt_csv))


# Loading data to postgresql database
def load_to_postgres_task(csv_file):
        # Connect to the database
        db_params = {
            'host': 'localhost',
            'database': 'us_debt',
            'user': 'postgres',
            'password': 'D2racine4ac#',
            'port': '5432'
        }
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Create the table
        '''
        cur.execute("""
            CREATE TABLE us_debt_01 (
                    period_in_office INT,
                    total_debt numeric,
                    president_name NAME 
            );
        """)
        '''

        # load the data from the csv file to the table
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                cur.execute(
                    "INSERT INTO us_debt_01 (period_in_office, total_debt, president_name) VALUES (%s, %s, %s)",
                    row
                )
            # cur.copy_from(f, 'us_debt_01', sep=',')


        # Commit the transaction
        conn.commit()

        # Close the connection
        cur.close()
        conn.close()

        logging.info('Data loaded to postgres successfully')

# Call the load_to_postgres function
load_to_postgres_task(us_debt_csv)

