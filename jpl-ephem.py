import numpy as np
import pandas as pd
import math as m
from matplotlib import pyplot as plt 
from datetime import datetime, timedelta
from fractions import Fraction as fr

from astropy import coordinates
import astropy.units as u
from astropy.time import Time
import astropy.coordinates.representation as r

from astropy.coordinates import solar_system_ephemeris
solar_system_ephemeris.set('jpl')

BASE_TIME = datetime(1958, 10, 13, 2, 0, 0)
TIME_ZERO = "1958-10-13 02:00:00"

sum_table = pd.read_excel("sum_table.xlsx") # Import data from excel spreadsheet
timestamps = sum_table["Time"] # Take the column of data labelled "Time"

def get_moon(time_input: list, attribute: str): # Returns dataframe of the position of the moon in terms of the specified attribute. Available for distance, right ascension, declination.
    
    coords_arr = []

    # Find the longitude of the body at t=0 to create offset
    longitude_offset = coordinates.get_body("moon", Time(TIME_ZERO, format="iso", scale="utc"), ephemeris="de432s")
    longitude_offset = longitude_offset.transform_to(coordinates.GeocentricMeanEcliptic())
    longitude_offset = np.deg2rad(longitude_offset.lon.value)

    for seconds in time_input: 

        # Turn time, which is in seconds, into year:month:day hr:min:sec
        new_time = BASE_TIME + timedelta(seconds=seconds)
        new_time = new_time.strftime("%Y-%m-%d %H:%M:%S")

        new_time = Time(new_time, format="iso", scale="utc") # Convert time input to astropy time
        coords = coordinates.get_body("moon", new_time, ephemeris="de432s") # Get coordinates
        coords.representation_type = "spherical" # Change coordinates to spherical
        coords = coords.transform_to(coordinates.GeocentricMeanEcliptic())

        if attribute.lower() == "distance": 
            coords_arr.append(coords.distance.value)
        elif attribute.lower() == "azimuth angle": 
            coords_arr.append(fr(1, 2) * np.pi - np.deg2rad(coords.lat.value))
        elif attribute.lower() == "polar angle": # We need to perform an offset for longitude to adjust for the different x-axis between the dataset and the calculated coordinates, and change the range to be 0 to 2pi instead of pi to -pi
            longitude = np.deg2rad(coords.lon.value) - longitude_offset
            if longitude < 0: 
                longitude = 2 * np.pi + longitude
            coords_arr.append(longitude)
    
    # Generate dataframe with data
    jpl_data = pd.DataFrame(coords_arr, columns=[attribute]) 
    jpl_data = pd.concat([timestamps, jpl_data], axis=1)

    return jpl_data

jpl_distance = get_moon(timestamps, "Distance")
jpl_az= get_moon(timestamps, "Azimuth Angle")
jpl_pol = get_moon(timestamps, "Polar Angle")

jpl_ephem = pd.concat([jpl_distance, jpl_pol, jpl_az], axis=1, join="inner") # Consolidate data
jpl_ephem = jpl_ephem.T.drop_duplicates().T # Drop duplicated columns

jpl_ephem.to_excel("jpl_ephem_transformed.xlsx")