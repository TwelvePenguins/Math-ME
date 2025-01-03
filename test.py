from astropy.coordinates import get_body, CartesianRepresentation, GCRS, BaseCoordinateFrame, FunctionTransformWithFiniteDifference, frame_transform_graph, TimeAttribute
from astropy.time import Time
import astropy.units as u
import numpy as np

# Step 1: Compute the Moon's position at the reference time
time_reference = Time('1958-10-13 02:00:00', scale='utc')
moon_position_reference = get_body('moon', time_reference)

# Convert to Cartesian coordinates
moon_cartesian_reference = moon_position_reference.cartesian

# Normalize the position vector to get the direction
x_axis_direction = moon_cartesian_reference / moon_cartesian_reference.norm()

# Step 2: Define a custom coordinate frame with obstime attribute
class CustomFrame(BaseCoordinateFrame):
    default_representation = CartesianRepresentation
    obstime = TimeAttribute(default=None)

# Define the rotation matrix to align the x-axis with the Moon's direction
def rotation_matrix_from_vectors(vec1, vec2):
    """Compute the rotation matrix that aligns vec1 to vec2."""
    a = vec1 / np.linalg.norm(vec1)
    b = vec2 / np.linalg.norm(vec2)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat @ kmat * ((1 - c) / (s ** 2))
    return rotation_matrix

# Identity vector along the x-axis
x_identity = np.array([1, 0, 0])

# Compute the rotation matrix
rotation_matrix = rotation_matrix_from_vectors(x_identity, x_axis_direction.xyz.value)

# Define the transformation function
def gcrs_to_custom(gcrs_coord, custom_frame):
    # Apply the rotation matrix to the GCRS coordinates
    rotated_coords = rotation_matrix @ gcrs_coord.cartesian.xyz.value
    return CustomFrame(CartesianRepresentation(rotated_coords, unit=u.km), obstime=gcrs_coord.obstime)

# Register the transformation
frame_transform_graph.add_transform(GCRS, CustomFrame, FunctionTransformWithFiniteDifference(gcrs_to_custom, fromsys=GCRS, tosys=CustomFrame))

# Step 3: Transform Moon's position to the new frame at a given time
def get_moon_position_in_custom_frame(time_str):
    time = Time(time_str, scale='utc')
    moon_position = get_body('moon', time)
    moon_position_custom = moon_position.transform_to(CustomFrame(obstime=time))
    return moon_position_custom.cartesian.xyz.to(u.km)

# Example usage
time_input = '1958-10-16 11:57:54'
moon_position_custom_frame = get_moon_position_in_custom_frame(time_input)
print(moon_position_custom_frame)
