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
RATE_OF_NODAL_PREC = -1.0704 * m.pow (10, -8) # Rate of nodal precession

# Omega values taken from table 1
OMEGA_VALUES = [0.27594, 1.6804, 2.3935, np.pi, 3.8530, 4.602809, 5.4162866, 0]
# The fraction of orbit the moon has completed when each of the above data points were calculated
FRACTION_OF_ORBIT = [fr(1, 8), fr(1, 4), fr(3, 8), fr(1, 2), fr(5, 8), fr(3, 4), fr(7, 8), 1]
# Column title for summary table initialised below
COLUMNS = ["Cycle", "Phase", "Time",
           "Spherical Coordinates", "Cartesian Coordinates", "Verify"]

# Arrays created to store plotting data
r_arr = np.array([]) # Initialising an empty numpy array to store r 

# Initialising a table for data storing
sum_table = pd.DataFrame(columns=COLUMNS)
print(sum_table)

for cycle in range(0, 24):  # For each orbit of the moon in 1098 years
    for phase in range(0, 8):  # For each of 8 points we calculate in each complete rotation
        time = LUNAR_PERIOD * FRACTION_OF_ORBIT[phase] + cycle * LUNAR_PERIOD # Time passed, t

        omega = OMEGA_VALUES[phase]
        r = round((SEMI_MAJOR_AXIS * (1 - m.pow(ECCENTRICITY, 2))) / (1 + ECCENTRICITY * np.cos(omega - RATE_OF_APS_PREC * time)), 5) # Equation 2.2
        beta = np.arcsin(-np.sin(ORBITAL_INCLINE) * (np.sin(RATE_OF_NODAL_PREC * time) * np.cos(omega) + np.cos(RATE_OF_NODAL_PREC * time) * np.sin(omega)))
        # print(beta)
        phi = round((fr(1, 2) * np.pi) - beta, 5)

        r_arr = np.append(r_arr, r) # add r to the r_arr

        spherical_coords = [] # Temporary variable to store spherical coords
        spherical_coords.append(r)
        spherical_coords.append(omega)
        spherical_coords.append(phi)

        x = round(r * np.sin(phi) * np.cos(omega), 5)
        y = round(r * np.sin(phi) * np.sin(omega), 5)
        z = round(r * np.cos(phi), 5)
        omega = round(omega, 5)

        cartesian_coords = []
        cartesian_coords.append(x)
        cartesian_coords.append(y)
        cartesian_coords.append(z)

        iteration = (phase + 1) + cycle * 8 # Which iteration produced these results

        if round(np.sqrt(m.pow(x, 2) + m.pow(y, 2) + m.pow(z, 2)), 5) == r :
            verification_status = True
        else: 
            verification_status = False


        new_df_row = pd.DataFrame(
            {
            "Cycle": cycle, 
            "Phase": phase + 1, 
            "Time": time, 
            "Spherical Coordinates": [spherical_coords], 
            "Cartesian Coordinates": [cartesian_coords], 
            "Verify": verification_status
            }, 
            index=[iteration]
        )

        sum_table = pd.concat([sum_table, new_df_row])

# Save to excel file
# sum_table.to_excel("sum_table.xlsx") 

print(sum_table)

# Plot with matplotlib
fig_r = plt.figure()
axes_t = fig_r.add_subplot()

fig_r = plt.plot(sum_table["Time"], r_arr)
fig_r = plt.ylabel("Lunar straight line distance from Earth / km")
fig_r = plt.xlabel("Time / s")

def annot_max(x,y):
    ymax = y.max()

    for i in y: 
        if i == ymax: 
            xmax = x[np.argmax(i)]
            text= "x={:.3f}, y={:.3f}".format(xmax, ymax)

            plt.annotate(text, 
                         (xmax, ymax), 
                         textcoords="offset points", 
                         xytext=(0,10), 
                         ha='center')

annot_max(np.array(sum_table["Time"]), r_arr)

plt.show()