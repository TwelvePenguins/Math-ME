import numpy as np

# Constants
factor = -1.0704 * 10**-8
value = 295074.36
angle = 0.27594

# Convert 5.145π/180 to radians
theta = 5.145 * np.pi / 180

# Calculate β
beta = np.arcsin(
    np.sin(theta) * (np.sin(factor * value) * np.cos(angle) - np.cos(factor * value) * np.sin(angle))
)

print(f"β = {beta}")
