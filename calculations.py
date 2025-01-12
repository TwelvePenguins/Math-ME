import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from fractions import Fraction as fr
import math as m

# Astrological constants
LUNAR_PERIOD = 2360594.88
ECCENTRICITY = 0.0549
SEMI_MAJOR_AXIS = 0.3844 * m.pow(10, 6)
RATE_OF_APS_PREC = 2.2496 * m.pow (10, -8) # Rate of apsidal precession
ORBITAL_INCLINE = np.deg2rad(5.145) # Convert incline to radians
RATE_OF_NODAL_PREC = 1.0704 * m.pow (10, -8) # Rate of nodal precession

# Omega values taken from table 1
OMEGA_VALUES = [0.27594, 1.6804, 2.3935, np.pi, 3.8530, 4.602809, 5.4162866, 0]
# The fraction of orbit the moon has completed when each of the above data points were calculated
FRACTION_OF_ORBIT = [fr(1, 8), fr(1, 4), fr(3, 8), fr(1, 2), fr(5, 8), fr(3, 4), fr(7, 8), 1]
# Column title for summary table initialised below
COLUMNS = ["Cycle", "Phase", "Time",
           "Distance", "Azimuth Angle", "Beta", "Polar Angle"]

# Arrays created to store plotting data
r_arr = np.array([]) # Initialising an empty numpy array to store r 

# Initialising a table for data storing
sum_table = pd.DataFrame(columns=COLUMNS)

for cycle in range(0, 241):  # For each orbit of the moon in 1098 years
    for phase in range(0, 8):  # For each of 8 points we calculate in each complete rotation
        time = LUNAR_PERIOD * FRACTION_OF_ORBIT[phase] + cycle * LUNAR_PERIOD # Time passed, t

        omega = OMEGA_VALUES[phase]
        r = round((SEMI_MAJOR_AXIS * (1 - m.pow(ECCENTRICITY, 2))) / (1 + ECCENTRICITY * np.cos(omega - RATE_OF_APS_PREC * time)), 5) # Equation 2.2
        beta = np.arcsin(np.sin(ORBITAL_INCLINE) * (np.sin(RATE_OF_NODAL_PREC * time) * np.cos(omega) + np.cos(RATE_OF_NODAL_PREC * time) * np.sin(omega)))
        phi = round((fr(1, 2) * np.pi) - beta, 5)

        r_arr = np.append(r_arr, r) # add r to the r_arr

        iteration = (phase + 1) + cycle * 8 # Which iteration produced these results

        new_df_row = pd.DataFrame(
            {
            "Cycle": cycle, 
            "Phase": phase + 1, 
            "Time": time, 
            "Distance": r,
            "Azimuth Angle": phi,
            "Beta": beta, 
            "Polar Angle": omega
            }, 
            index=[iteration]
        )

        sum_table = pd.concat([sum_table, new_df_row])

# Save to excel file
sum_table.to_excel("sum_table.xlsx") 

print(sum_table)

# Plot with matplotlib
def plot_graph(key: str): 
    y_label = ""
    key_array = sum_table[key]

    fig_r = plt.figure()
    fig_r.add_subplot()

    fig_r = plt.plot(sum_table["Time"], key_array)
    fig_r = plt.xlabel("Time / s")
    fig_r = plt.ylabel(y_label)

    if key == "Distance": 
        y_label = "Lunar straight line distance from Earth / km"
    elif key == "Polar Angle": 
        y_label = "Polar Angle / radians"
    elif key == "Azimuth Angle": 
        y_label = "Azimuth Angle / radians"
    
    # Labelling the maximum
    y_max = max(key_array)

    for i in range(0, len(key_array) - 1):
        if key_array.iloc[i] == y_max: 
            print(key_array.iloc[i])
            x_max = sum_table["Time"].iloc[i]
            text= "x={:.3f}, y={:.3f}".format(x_max, y_max)
            plt.plot([x_max], [y_max], "o")
            plt.annotate(text, 
                         (x_max, y_max), 
                         textcoords="offset points", 
                         xytext=(0,10), 
                         ha='center')
            
    # Labelling the minimum
    y_min = min(key_array)

    for i in range(0, len(key_array) - 1):
        if key_array.iloc[i] == y_min: 
            print(key_array.iloc[i])
            x_min = sum_table["Time"].iloc[i]
            text= "x={:.3f}, y={:.3f}".format(x_min, y_min)
            plt.plot([x_min], [y_min], "o")
            plt.annotate(text, 
                         (x_min, y_min), 
                         textcoords="offset points", 
                         xytext=(0,-20), 
                         ha='center')
    
    plt.show()

plot_graph("Distance")