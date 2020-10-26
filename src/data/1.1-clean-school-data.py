import os
import json 
import pandas as pd
import numpy as np

from convert_address_to_lat_long import get_lat_long

data_dir = 'data'

filenames = [
    'primary-school.json',
    'secondary-school.json'
]

def main(filename, raw_dir='raw', processed_dir='processed'):
    
    # Read dataset
    with open(os.path.join(data_dir, raw_dir, filename)) as f:
        data = json.load(f)

    # Filter columns
    data = pd.json_normalize(data['response']['docs'])
    data = data[[
        'school_name',
        'type_s',
        'school_type_ss',
        'school_nature_s',
        'school_area_s',
        'address_s',
        'postal_code_s',
        'location_p',
    ]]

    # Cleaning data
    data['school_type_ss'] = data['school_type_ss'].apply(lambda x: x[0])
    
    location = data['location_p'].apply(lambda x: x[0].split(',') if isinstance(x, list) else [np.nan, np.nan])
    lat = location.apply(lambda x: x[0])
    long = location.apply(lambda x: x[1])

    data['location_p_lat'] = lat
    data['location_p_long'] = long
    data = data.drop('location_p', axis=1)

    # Update columns
    data.columns = [
        'school_name',
        'school_category',
        'school_type',
        'school_nature',
        'school_area',
        'school_address',
        'school_postal_code',
        'school_lat',
        'school_long'
    ]

    filename = filename.replace('.json', '.csv')
    data.to_csv(os.path.join(data_dir, processed_dir, filename), index=False)

if __name__ == "__main__":
    for filename in filenames:
        main(filename)