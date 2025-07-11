import streamlit as st
import math

st.title("📡 Microstrip Patch Antenna Calculator")

# Inputs
freq_ghz = st.number_input("Operating Frequency (GHz)", min_value=0.1, max_value=100.0, value=2.4)
er = st.number_input("Dielectric Constant (εr)", min_value=1.0, value=4.4)
h_mm = st.number_input("Substrate Thickness (mm)", min_value=0.1, value=1.6)

if st.button("Calculate"):

    # Convert to SI
    f = freq_ghz * 1e9
    h = h_mm / 1000  # mm to m
    c = 3e8

    # Patch Width
    W = (c / (2 * f)) * math.sqrt(2 / (er + 1))

    # Effective Dielectric Constant
    e_eff = (er + 1)/2 + ((er - 1)/2) * (1 + 12 * (h / W))**-0.5

    # Extension length ΔL
    delta_L = 0.412 * h * ((e_eff + 0.3) * ((W / h) + 0.264)) / ((e_eff - 0.258) * ((W / h) + 0.8))

    # Actual Length
    L = (c / (2 * f * math.sqrt(e_eff))) - 2 * delta_L

    st.markdown("### 📐 Patch Dimensions")
    st.write(f"**Patch Width (W):** {W*1000:.2f} mm")
    st.write(f"**Effective εr:** {e_eff:.4f}")
    st.write(f"**Fringing Length (ΔL):** {delta_L*1000:.4f} mm")
    st.write(f"**Patch Length (L):** {L*1000:.2f} mm")

    st.markdown("📎 *Equations based on standard rectangular patch design (fringing fields accounted).*")
