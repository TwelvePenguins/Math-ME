# TwelvePenguins' Mathematical Exploration
> Topic: Mathematically modelling the lunar orbit

## What in the tarnation is this doing on GitHub?
Repository for my math exploration project, which is to be submitted for the International Baccalaureate degree. <br>
It does not make sense on its own without the report, which is not available publically. <br>
Meant for personal future reference and not suitable for general public use. 

## Files and their uses
1. `calculations.py` contains my personal formula for calculating the spherical coordinates of the Moon over 20 years, taking 8 discreet datapoints per orbit and plotting them in a continuous graph.
2. `sum_table.xlsx` contains the results previously calculated. 
3. `jpl_ephem.py` contains the code to retrieve ephemeris through [astro.py](https://www.astropy.org/).
4. `jpl_ephem.xlsx` contains the raw data retrieved that was not transformed to suit the starting time of the simulation. 
5. `jpl_ephem_transformed.xlsx` is the above but transformed to be more suitable for error-checking
6. `checking.py` contains the code to compare the retrieved data and the calculated results, outputting a percentage error. 

## Copyright Information
Since this is somewhat sensitive in the sense that I am submitting this for a diploma, I just want to reiterate that no liscence has been chosen for this repository, which means that this is not open source and **cannot be redistributed.**