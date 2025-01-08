import pandas as pd
import numpy as np

# Import data from excel spreadsheet
sum_table = pd.read_excel("sum_table.xlsx") 
jpl_ephem = pd.read_excel("jpl_ephem_transformed.xlsx") 

def find_error(key: str): # Only accept sum_table and jpl_ephem comparisons
    if len(sum_table.index) == len(jpl_ephem.index): 
        
        calc_attribute = sum_table[key]
        jpl_attribute = jpl_ephem[key]
        error = 0

        for i in range(0, len(jpl_ephem.index)):
            if key == "Polar Angle": 
                error += min(abs(calc_attribute[i] - jpl_attribute[i]), 2*np.pi - abs(calc_attribute[i] - jpl_attribute[i])) # Find minimum between the angle and reflex angle between two angles
            else: 
                error += abs(calc_attribute[i] - jpl_attribute[i])


        avg_error = error / len(calc_attribute)
        avg_jpl = np.mean(jpl_attribute)
        error_percentage = (avg_error / avg_jpl) * 100
        
        print(f"The error for {key} is {error_percentage}%.")

    else: 
        print("Error: Unequal number of rows")

find_error("Distance")
find_error("Azimuth Angle")
find_error("Polar Angle")