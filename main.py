import numpy as np
import matplotlib.pyplot as plt
import math
import streamlit as st

st.session_state.setdefault("box_width", 235)
st.session_state.setdefault("box_height", 239)
st.session_state.setdefault("maximaliseer_breedte", False)
st.session_state.setdefault("maximaliseer_hoogte", False)
st.session_state.setdefault("max_breedte", 5)
st.session_state.setdefault("max_hoogte", 5)

# Streamlit UI voor interactieve parameterselectie
st.title("Balken stapelen")
diameters = {
    8: "8cm",
    9: "9cm",
    10: "10cm (gefreesde balken tot 6m)",
    11: "11cm",
    12: "12cm (8m gefreesde balken)",
    13: "13cm",
    14: "14cm",
    15: "15cm"
}
st.session_state.diameter = st.radio(
    "Diameter van balk (cm)", 
    options=list(diameters.keys()),
    format_func=lambda x: diameters[x],
    index=2
)
radius = st.session_state.diameter / 2

st.markdown("---")


# Radiobutton for selecting box/container dimensions
options = [
    "Standaard container (binnenmaten: 235cm x 239cm)", # actually 239,3 cm
    "Container offerte 2015 (binnenmaten: 238cm x 220cm)",
    "Aangepast",
]
option = st.radio(
    "Selecteer vak/container type",
    options=options,
)

col1, col2 = st.columns(2)
if option == options[0]:
    with col1:
        box_width = st.number_input("Vak/container breedte (cm)", min_value=1, step=1, value=235, disabled=True)
        st.session_state.box_width = box_width
    with col2:
        box_height = st.number_input("Vak/container hoogte (cm)", min_value=1, step=1, value=239, disabled=True)
        st.session_state.box_height = box_height
elif option == options[1]:
    with col1:
        box_width = st.number_input("Vak/container breedte (cm)", min_value=1, step=1, value=238, disabled=True)
        st.session_state.box_width = box_width
    with col2:
        box_height = st.number_input("Vak/container hoogte (cm)", min_value=1, step=1, value=220, disabled=True)
        st.session_state.box_height = box_height
else:
    with col1:
        box_width = st.number_input("Vak/container breedte (cm)", min_value=1, step=1, value=st.session_state.box_width)
    with col2:
        box_height = st.number_input("Vak/container hoogte (cm)", min_value=1, step=1, value=st.session_state.box_height)


st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    maximaliseer_breedte = st.checkbox("Maximaliseer in breedte")
    if maximaliseer_breedte:
        aantal_buizen_breedte = max(1, int(box_width // (2 * radius)))
        st.number_input("Aantal balken in de breedte", min_value=1, step=1, value=aantal_buizen_breedte, disabled=True)
    else:
        aantal_buizen_breedte = st.number_input("Aantal balken in de breedte", min_value=1, step=1, value=st.session_state.max_breedte)
    st.session_state.max_breedte = aantal_buizen_breedte

with col2:
    maximaliseer_hoogte = st.checkbox("Maximaliseer in hoogte")
    if maximaliseer_hoogte:
        aantal_buizen_hoogte = max(0, int((box_height - 2 * radius) // (math.sqrt(3) * radius))) + 1
        st.number_input("Aantal balken in de hoogte", min_value=1, step=1, value=aantal_buizen_hoogte, disabled=True)
    else:
        aantal_buizen_hoogte = st.number_input("Aantal balken in de hoogte", min_value=1, step=1, value=st.session_state.max_hoogte)
    st.session_state.max_hoogte = aantal_buizen_hoogte

# Update Matplotlib font settings to match Streamlit
plt.rcParams.update({
    "font.size": 12,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans", "sans-serif"],
    "axes.labelsize": 14,
    "axes.titlesize": 16,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

# Berekeningen
breedte = 2 * radius * aantal_buizen_breedte
hoogte = (math.sqrt(3) * radius) * (aantal_buizen_hoogte - 1) + 2 * radius
totaal_aantal = aantal_buizen_breedte * aantal_buizen_hoogte - (aantal_buizen_hoogte // 2)

# Weergave van de berekende resultaten
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Breedte**: {breedte:.2f} cm")
with col2:
    st.write(f"**Hoogte**: {hoogte:.2f} cm")

st.markdown("---")


## other
# Visualize with Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))  # Vaste figuurgrootte voor consistente schaal
ax.set_aspect('equal', adjustable='datalim')
ax.set_xlim(-5, 300)  # Stel vaste x-as in van 0 tot 300 cm
ax.set_ylim(-5, 300)  # Stel vaste y-as in van 0 tot 300 cm
# Add the total number of beams to the plot
ax.text(0.5, 1.05, f"Totaal: {totaal_aantal} balken", transform=ax.transAxes, ha='center', va='center', fontsize=12, color='black', fontweight='bold')


# Precompute values for circle positioning
sqrt3_radius = math.sqrt(3) * radius
x_positions = []
y_positions = []

    # Calculate positions for each circle and store them
for row in range(aantal_buizen_hoogte):
    y_offset = row * sqrt3_radius + radius
    for col in range(aantal_buizen_breedte - (row % 2)):
        x_offset = 2 * radius * (col + 0.5 * (row % 2)) + radius
        
        # Only add positions for circles within the 300x300 area
        if x_offset + radius <= 300 and y_offset + radius <= 300:
            x_positions.append(x_offset)
            y_positions.append(y_offset)

diameter_in_points = ( radius) * 2.9 
s = diameter_in_points ** 2

# Draw all circles at once using scatter for faster rendering
ax.scatter(x_positions, y_positions, s=s, facecolors='none', edgecolors="blue")

# Add a rectangle to the plot representing the box
rect = plt.Rectangle((-0.5, -0.5), box_width + 0.5, box_height + 1.7, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

# Aslabels toevoegen met eenheden
ax.set_xlabel("Breedte (cm)")
ax.set_ylabel("Hoogte (cm)")

# Display the plot in Streamlit
st.pyplot(fig)
