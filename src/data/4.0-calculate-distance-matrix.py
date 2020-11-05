import os
import time
import random
import argparse

import pandas as pd
import numpy as np

from math import radians, cos, sin, asin, sqrt
from os.path import dirname

import logging

# raw & processed dir
processed_dir = os.path.join(os.getcwd(), 'data', 'processed')
distance_dir = os.path.join(os.getcwd(), 'data', 'distance')

# logging basic configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filemode='w')

# GeekForGeek
# Note: lat1, lat2, lon1, lon2 must be in radian form
def dist_between_points(lat1, lat2, lon1, lon2):
	# Haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a))

	# Radius of earth in kilometers. Use 3956 for miles
	r = 6371

	# calculate the result
	return(c * r)

def main(origin_filename, destination_filename):
    # Load datasets
    origin_df = pd.read_csv(os.path.join(processed_dir, origin_filename))
    dist_df = pd.read_csv(os.path.join(processed_dir, destination_filename))

    logging.info(f"Number of Origin: {origin_df.shape[0]}")
    logging.info(f"Number of Destination: {dist_df.shape[0]}")

    # Transform the lat & lon to radian
    origin_df['lat_rad'] = origin_df['lat'].apply(lambda x: radians(x))
    origin_df['long_rad'] = origin_df['long'].apply(lambda x: radians(x))

    dist_df['lat_rad'] = dist_df['lat'].apply(lambda x: radians(x))
    dist_df['long_rad'] = dist_df['long'].apply(lambda x: radians(x))

    # Get lat long
    dist_matrix = []
    for o_lat, o_long in zip(origin_df['lat_rad'], origin_df['long_rad']):
        distance = [dist_between_points(o_lat, o_long, d_lat, d_long) for d_lat, d_long
                        in zip(dist_df['lat_rad'], dist_df['long_rad'])]

        dist_matrix.append(distance)

    logging.info(f"Saving Numpy Matrix...")
    dist_matrix = np.array(dist_matrix)
    destination_filename = f'distance-{destination_filename.replace(".csv", ".npz")}'

    logging.info(f"Matrix Shape: {dist_matrix.shape}")
    with open(os.path.join(distance_dir, destination_filename), 'wb') as f:
        np.save(f, dist_matrix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-origin_file", help="Define the dataset size (e.g. small or full)", required=True)
    parser.add_argument("-destination_file", help="Define the dataset size (e.g. small or full)", required=True)

    args = parser.parse_args()
    main(args.origin_file, args.destination_file)
