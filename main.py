import numpy as np
import matplotlib.pyplot as plt
import math
import streamlit as st

st.session_state.setdefault("box_width", 235.0)
st.session_state.setdefault("box_height", 239.3)
st.session_state.setdefault("maximaliseer_breedte", False)
st.session_state.setdefault("maximaliseer_hoogte", False)


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
    "Standaard container (binnenmaten: 235 x 239 cm)",
    "Container offerte 2015 (binnenmaten: 238 x 220 cm)",
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
    with col2:
        box_height = st.number_input("Vak/container hoogte (cm)", min_value=1, step=1, value=239, disabled=True)
elif option == options[1]:
    st.write("option[1]")
    with col1:
        box_width = st.number_input("Vak/container breedte (cm)", min_value=1, step=1, value=238, disabled=True)
    with col2:
        box_height = st.number_input("Vak/container hoogte (cm)", min_value=1, step=1, value=220, disabled=True)
else:
    with col1:
        box_width = st.number_input("Vak/container breedte (cm)", min_value=1, step=1, value=st.session_state.box_width)
    with col2:
        box_height = st.number_input("Vak/container hoogte (cm)", min_value=1, step=1, value=st.session_state.box_height)

st.session_state.box_width = box_width
st.session_state.box_height = box_height

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    maximaliseer_breedte = st.session_state.maximaliseer_breedte
    if maximaliseer_breedte:
        aantal_buizen_breedte = max(1, int(box_width // (2 * radius)))
        st.number_input("Aantal balken in de breedte", min_value=1, step=1, value=aantal_buizen_breedte, disabled=True)
    else:
        aantal_buizen_breedte = st.number_input("Aantal balken in de breedte", min_value=1, step=1, value=5)
    maximaliseer_breedte = st.checkbox("Maximaliseer in breedte")
    if st.session_state.maximaliseer_breedte != maximaliseer_breedte:
        #trigger update ui
        st.session_state.maximaliseer_breedte = maximaliseer_breedte
        st.rerun()

with col2:
    maximaliseer_hoogte = st.session_state.maximaliseer_hoogte
    if maximaliseer_hoogte:
        aantal_buizen_hoogte = max(1, int(box_height // (math.sqrt(3) * radius)))
        st.number_input("Aantal balken in de hoogte", min_value=1, step=1, value=aantal_buizen_hoogte, disabled=True)
    else:
        aantal_buizen_hoogte = st.number_input("Aantal balken in de hoogte", min_value=1, step=1, value=5)
    maximaliseer_hoogte = st.checkbox("Maximaliseer in hoogte")
    if st.session_state.maximaliseer_hoogte != maximaliseer_hoogte:
        #trigger update ui
        st.session_state.maximaliseer_hoogte = maximaliseer_hoogte
        st.rerun()



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

# Visualisatie met Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))  # Vaste figuurgrootte voor consistente schaal
ax.set_aspect('equal', adjustable='datalim')
ax.set_xlim(-1, 300)  # Stel vaste x-as in van 0 tot 300 cm
ax.set_ylim(-4, 300)  # Stel vaste y-as in van 0 tot 300 cm

# Add the total number of beams to the plot
ax.text(0.5, 1.05, f"Totaal Aantal: {totaal_aantal}", transform=ax.transAxes, ha='center', va='center', fontsize=12, color='black', fontweight='bold')

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
