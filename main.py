import numpy as np
import matplotlib.pyplot as plt
import math
import streamlit as st

# Streamlit UI voor interactieve parameterselectie
st.title("Interactieve balkenstapel visualisatie")
diameter = st.radio(
    "Diameter van balk (cm)", 
    options=[10, 11, 12, 13], 
    format_func=lambda x: {
        8: "8cm",
        9: "9cm",
        10: "10cm (gefreesde balken tot 6m)",
        11: "11cm",
        12: "12cm (8m gefreesde balken)",
        13: "13cm",
        14: "14cm",
        15: "15cm"
    }[x],
    index=0
)
radius = diameter / 2
aantal_buizen_breedte = st.number_input("Aantal balken in breedte", min_value=1, step=1, value=5)
aantal_buizen_hoogte = st.number_input("Aantal balken in hoogte", min_value=1, step=1, value=5)


# Radiobutton for selecting box/container dimensions
option = [
    "Standaard (binnenmaten: 235 x 239.3 cm)", 
    "Container offerte 2015 (binnenmaten: 238 x 220 cm)", 
    "Aangepast"
]
box_option = st.radio(
    "Selecteer vak/container type",
    options=option,
)

if box_option == option[0]:
    box_width = st.number_input("Vak/container breedte (cm)", min_value=1.0, step=1.0, value=235.0, disabled=True)
    box_height = st.number_input("Vak/container hoogte (cm)", min_value=1.0, step=1.0, value=239.3, disabled=True)
elif box_option == option[1]:
    box_width = st.number_input("Vak/container breedte (cm)", min_value=1.0, step=1.0, value=238.0, disabled=True)
    box_height = st.number_input("Vak/container hoogte (cm)", min_value=1.0, step=1.0, value=220.0, disabled=True)
else:
    box_width = st.number_input("Vak/container breedte (cm)", min_value=1.0, step=1.0, value=235.0)
    box_height = st.number_input("Vak/container hoogte (cm)", min_value=1.0, step=1.0, value=239.3)

# Berekeningen
breedte = 2 * radius * aantal_buizen_breedte
hoogte = (math.sqrt(3) * radius) * (aantal_buizen_hoogte - 1) + 2 * radius
totaal_aantal = aantal_buizen_breedte * aantal_buizen_hoogte - (aantal_buizen_hoogte // 2)

# Weergave van de berekende resultaten
st.write(f"**Breedte**: {breedte} cm")
st.write(f"**Hoogte**: {hoogte} cm")
st.write(f"**Totaal Aantal**: {totaal_aantal}")

# Visualisatie met Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))  # Vaste figuurgrootte voor consistente schaal
ax.set_aspect('equal', adjustable='datalim')
ax.set_xlim(-1, 300)  # Stel vaste x-as in van 0 tot 300 cm
ax.set_ylim(-4, 300)  # Stel vaste y-as in van 0 tot 300 cm

# Aslabels toevoegen met eenheden
ax.set_xlabel("Breedte (cm)")
ax.set_ylabel("Hoogte (cm)")

# Add a rectangle to the plot representing the box
rect = plt.Rectangle((0, 0), box_width, box_height, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

# Cirkelplot in een hexagonaal stapelpatroon
for rij in range(aantal_buizen_hoogte):
    y_offset = rij * math.sqrt(3) * radius + radius
    for kolom in range(aantal_buizen_breedte - (rij % 2)):
        x_offset = 2 * radius * (kolom + 0.5 * (rij % 2)) + radius
        
        # Controleer of de cirkel volledig binnen het 300x300 gebied past
        if (x_offset + radius <= 300) and (y_offset + radius <= 300):
            cirkel = plt.Circle((x_offset, y_offset), radius, edgecolor="blue", fill=False)
            ax.add_patch(cirkel)

# Display the plot with the added rectangle
st.pyplot(fig)
