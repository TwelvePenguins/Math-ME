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
coords_arr = []

sum_table = pd.read_excel("sum_table.xlsx") # Import data from excel spreadsheet
timestamps = sum_table["Time"] # Take the column of data labelled "Time"

print(timestamps)

def get_moon(time_input: list):

    for seconds in time_input: 
        # Turn time, which is in seconds, into year:month:day hr:min:sec
        new_time = base_time + timedelta(seconds=seconds)
        new_time = new_time.strftime("%Y-%m-%d %H:%M:%S")

        new_time = Time(new_time, format="iso", scale="utc") # Convert time input to astropy time
        coords = coordinates.get_body("moon", new_time, ephemeris="de432s") # Get coordinates
        coords.representation_type = "spherical" # Change coordinates to spherical
        coords_arr.append(coords.distance.value)

    return coords_arr

jpl_distances = pd.DataFrame(get_moon(timestamps), columns=["Distance"])
jpl_distances = pd.concat(timestamps, jpl_distances)

print(jpl_distance)