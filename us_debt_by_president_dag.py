# Import necessary modules

import sys
import os
import logging
import logging.handlers
import requests
import pendulum
import pandas as pd
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
us_debt_csv = '/Users/jbshome/Desktop/us_debt/us_debt.csv'

# Url to fetch the data
url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_outstanding?fields=record_fiscal_year, debt_outstanding_amt&sort=-record_fiscal_year&format=json&page[number]=1&page[size]=235'
# Path to csv file
us_debt_csv = '/Users/jbshome/Desktop/us_debt_etl_pipeline/csv_files/us_debt_by_president.csv'

# Define the first task in the DAG.
# This task will extract data from an api
def extract_task(api_url):
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

# Call the extract_task function
df = extract_task(url)

# Define the second task in the DAG.
# This task will transform the data
def transform_task(data):
# Transform the data
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

    logging.info('Data transformed successfully')
    return data

# Call the extract_task function
cleaned_df = transform_task(df)

# Define the third task in the DAG.
# This task will load the data to a csv file
def load_task(df, csv_file):
    # Save to csv
    df.to_csv(csv_file, index=False)
    logging.info('Data saved to csv successfully')
    return df

# Call the load_task function
load_task(cleaned_df, us_debt_csv)