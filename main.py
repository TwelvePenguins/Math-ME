from astropy import coordinates
import astropy.units as u
from astropy.time import Time
import astropy.coordinates.representation as r

from astropy.coordinates import solar_system_ephemeris
solar_system_ephemeris.set('jpl')

# coords = coordinates.get_body("moon", Time("1958-10-16 11:57:54"))

# coords.representation_type = "cartesian"
# moon_cartesian = coords.cartesian.xyz.to(u.km)

# print(moon_cartesian)

def get_moon(time_input): 
    time = Time(time_input, format="iso", scale="utc")
    coords = coordinates.get_body("moon", time, ephemeris="de432s")
    coords.representation_type = "cartesian"
    moon_cartesian = coords.cartesian.xyz.to(u.km)

    print(moon_cartesian)

get_moon("1958-10-16 11:57:54")
get_moon("1958-10-13 02:00:00")
get_moon("1958-10-09 17:03:06")

# class MyFrame1(BaseCoordinateFrame):
#     # Specify how coordinate values are represented when outputted
#     default_representation = r.SphericalRepresentation
