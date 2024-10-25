import numpy as np
import matplotlib.pyplot as plt
import math
import streamlit as st

# Streamlit UI for interactive parameter selection
st.title("Interactive Circle Stack Visualization")
diameter = st.slider("Diameter of Circles (cm)", 8, 16, 10)  # default to 10cm
radius = diameter / 2
num_pipes_width = st.number_input("Number of Pipes in Width", min_value=1, step=1, value=5)
num_pipes_height = st.number_input("Number of Pipes in Height", min_value=1, step=1, value=5)

# Calculations
width = 2 * radius * num_pipes_width
height = (math.sqrt(3) * radius) * (num_pipes_height - 1) + 2 * radius
total_count = num_pipes_width * num_pipes_height - (num_pipes_height // 2)

# Display calculated results
st.write(f"**Width (Breedte)**: {width} cm")
st.write(f"**Height (Hoogte)**: {height} cm")
st.write(f"**Total Count (Aantal)**: {total_count}")

# Visualization using Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))  # Fixed figure size for consistent scaling
ax.set_aspect('equal', adjustable='datalim')
ax.set_xlim(-1, 300)  # Set fixed x-axis from 0 to 300 cm
ax.set_ylim(-1, 300)  # Set fixed y-axis from 0 to 300 cm

# Add axis labels with units
ax.set_xlabel("Width (cm)")
ax.set_ylabel("Height (cm)")

# Plot circles in a hexagonal stacking pattern
for row in range(num_pipes_height):
    y_offset = row * math.sqrt(3) * radius + radius
    for col in range(num_pipes_width - (row % 2)):
        x_offset = 2 * radius * (col + 0.5 * (row % 2)) + radius
        
        # Check if circle fits entirely within the 300x300 area
        if (x_offset + radius <= 300) and (y_offset + radius <= 300):
            circle = plt.Circle((x_offset, y_offset), radius, edgecolor="blue", fill=False)
            ax.add_patch(circle)

st.pyplot(fig)
