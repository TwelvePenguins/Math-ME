import numpy as np
import pandas as pd
import math as m
from datetime import datetime, timedelta

from astropy import coordinates
import astropy.units as u
from astropy.time import Time
import astropy.coordinates.representation as r

from astropy.coordinates import solar_system_ephemeris
solar_system_ephemeris.set('jpl')

base_time = datetime(1958, 10, 13, 2, 0, 0)

sum_table = pd.read_excel("sum_table.xlsx") # Import data from excel spreadsheet
timestamps = sum_table["Time"] # Take the column of data labelled "Time"
calc_distances = sum_table[["Time", "Spherical Coordinates"]] # Import the calculated data from the excel

print(timestamps)

def get_moon(time_input: list, attribute: str): # Returns dataframe of the position of the moon in terms of the specified attribute. Available for distance, right ascension, declination.
    
    coords_arr = []

    for seconds in time_input: 

        # Turn time, which is in seconds, into year:month:day hr:min:sec
        new_time = base_time + timedelta(seconds=seconds)
        new_time = new_time.strftime("%Y-%m-%d %H:%M:%S")

        new_time = Time(new_time, format="iso", scale="utc") # Convert time input to astropy time
        coords = coordinates.get_body("moon", new_time, ephemeris="de432s") # Get coordinates
        coords.representation_type = "spherical" # Change coordinates to spherical

        if attribute.lower() == "distance": 
            coords_arr.append(coords.distance.value)
        elif attribute.lower() == "ra": 
            coords_arr.append(np.deg2rad(coords.ra.value))
        elif attribute.lower() == "dec": 
            coords_arr.append(np.deg2rad(coords.dec.value))
    
    # Generate dataframe with data
    jpl_data = pd.DataFrame(coords_arr, columns=[attribute]) 
    jpl_data = pd.concat([timestamps, jpl_data], axis=1)

    return jpl_data

jpl_distance = get_moon(timestamps, "Distance")
jpl_ra = get_moon(timestamps, "RA")
jpl_dec = get_moon(timestamps, "Dec")

jpl_ephem = pd.concat([jpl_distance, jpl_ra, jpl_dec], axis=1, join="inner") # Consolidate data
jpl_ephem = jpl_ephem.T.drop_duplicates().T # Drop duplicated columns

jpl_ephem.to_excel("jpl_ephem.xlsx")