# app.py

import math
import streamlit as st

def calculate_inductance(frequency_mhz, capacitance_pf):
    frequency_hz = frequency_mhz * 1e6
    capacitance_f = capacitance_pf * 1e-12
    inductance_h = 1 / ((2 * math.pi * frequency_hz) ** 2 * capacitance_f)
    return inductance_h * 1e6  # µH

def wheeler_formula(inductance_uh, wire_diameter_mm):
    wire_diameter_in = wire_diameter_mm / 25.4
    for d_in in [i * 0.1 for i in range(2, 20)]:
        for n in range(2, 100):
            l_in = n * wire_diameter_in
            L_calc = (d_in ** 2 * n ** 2) / (18 * d_in + 40 * l_in)
            if abs(L_calc - inductance_uh) < 0.1:
                return {
                    "diameter_in": round(d_in, 3),
                    "diameter_mm": round(d_in * 25.4, 2),
                    "turns": n,
                    "length_mm": round(l_in * 25.4, 2)
                }
    return None

# Streamlit UI
st.title("🔧 LC Tuning Circuit Designer")

band = st.selectbox("Select band", ["FM", "AM", "Custom"])

if band == "FM":
    freq_min = 88
    freq_max = 108
elif band == "AM":
    freq_min = 0.535
    freq_max = 1.605
else:
    freq_min = st.number_input("Enter minimum frequency (MHz):", min_value=0.01)
    freq_max = st.number_input("Enter maximum frequency (MHz):", min_value=freq_min)

cap_min_pf = st.number_input("Variable capacitor min (pF):", min_value=1.0)
cap_max_pf = st.number_input("Variable capacitor max (pF):", min_value=cap_min_pf)
wire_diameter_mm = st.number_input("Copper wire diameter (mm):", min_value=0.1)

if st.button("Calculate"):
    L_max = calculate_inductance(freq_min, cap_max_pf)
    L_min = calculate_inductance(freq_max, cap_min_pf)

    st.markdown(f"### 📏 Required Inductance Range: `{round(L_min, 2)} µH` to `{round(L_max, 2)} µH`")

    st.markdown("#### Coil Parameters for L_min:")
    coil_min = wheeler_formula(L_min, wire_diameter_mm)
    if coil_min:
        st.json(coil_min)
    else:
        st.error("❌ Could not find suitable coil dimensions for L_min.")

    st.markdown("#### Coil Parameters for L_max:")
    coil_max = wheeler_formula(L_max, wire_diameter_mm)
    if coil_max:
        st.json(coil_max)
    else:
        st.error("❌ Could not find suitable coil dimensions for L_max.")
