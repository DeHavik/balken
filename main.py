import numpy as np
import matplotlib.pyplot as plt
import math
import streamlit as st

# Streamlit UI voor interactieve parameterselectie
st.title("Interactieve Balkenstapel visualisatie")
diameter = st.radio("Diameter van balk (cm)", options=[10, 11, 12, 13], index=0)  # standaard 10 cm
radius = diameter / 2
aantal_buizen_breedte = st.number_input("Aantal balken in breedte", min_value=1, step=1, value=5)
aantal_buizen_hoogte = st.number_input("Aantal balken in hoogte", min_value=1, step=1, value=5)

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
ax.set_ylim(-1, 300)  # Stel vaste y-as in van 0 tot 300 cm

# Aslabels toevoegen met eenheden
ax.set_xlabel("Breedte (cm)")
ax.set_ylabel("Hoogte (cm)")

# Cirkelplot in een hexagonaal stapelpatroon
for rij in range(aantal_buizen_hoogte):
    y_offset = rij * math.sqrt(3) * radius + radius
    for kolom in range(aantal_buizen_breedte - (rij % 2)):
        x_offset = 2 * radius * (kolom + 0.5 * (rij % 2)) + radius
        
        # Controleer of de cirkel volledig binnen het 300x300 gebied past
        if (x_offset + radius <= 300) and (y_offset + radius <= 300):
            cirkel = plt.Circle((x_offset, y_offset), radius, edgecolor="blue", fill=False)
            ax.add_patch(cirkel)

st.pyplot(fig)
