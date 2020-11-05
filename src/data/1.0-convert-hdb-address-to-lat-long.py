import os
import time
import random

import pandas as pd

from os.path import dirname
from utils import get_lat_long

import logging

# raw & processed dir
raw_dir = os.path.join(os.getcwd(), 'data', 'raw')
processed_dir = os.path.join(os.getcwd(), 'data', 'processed')

# logging basic configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filemode='w')

def main(filename):
    # Load datasets
    df = pd.read_csv(os.path.join(raw_dir, filename))

    # Corner cases
    df['street_name'] = df['street_name'].str.replace("ST. GEORGE'S LANE", "SAINT GEORGE LANE")

    # Construct full address
    df['full_address'] = df['block'] + ' ' + df['street_name'] + ' Singapore'

    logging.info(f"Dataset Size: {df.shape[0]}")

    # Get lat long
    status, lats, longs = [], [], []
    for index, address in enumerate(df['full_address']):
        if index % 1000 == 0:
            logging.info(f"Processed {index} records...")

        s, lat, long = get_lat_long(address)

        status.append(s)
        lats.append(lat)
        longs.append(long)

    # Append latitude & longitude
    df['status'] = status
    df['lat'] = lats
    df['long'] = longs

    logging.info(f"Saving Dataset...")

    df.to_csv(os.path.join(processed_dir, filename), index=False)


if __name__ == "__main__":
    main('resale-flat-prices-2017.csv')
