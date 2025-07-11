import streamlit as st
import math

st.set_page_config(page_title="Electronics Toolbox", layout="centered")
st.title("🧰 Electronics Toolbox")
st.markdown("### Choose a tool to begin:")

# --- Tool Icons as Buttons ---
col1, col2 = st.columns(2)
with col1:
    lc_click = st.button("🌀 LC Tuning", use_container_width=True)
with col2:
    patch_click = st.button("📡 Patch Antenna", use_container_width=True)

# Control tool selection via state
if "tool" not in st.session_state:
    st.session_state.tool = None
if lc_click:
    st.session_state.tool = "lc"
if patch_click:
    st.session_state.tool = "patch"

# ============================ TOOL 1: LC TUNING ============================
if st.session_state.tool == "lc":
    st.subheader("🌀 LC Tuning Circuit Designer")

    band = st.selectbox("Select Band", ["FM", "AM", "Custom"])

    if band == "FM":
        freq_min, freq_max = 88, 108
    elif band == "AM":
        freq_min, freq_max = 0.535, 1.605
    else:
        freq_min = st.number_input("Enter Min Frequency (MHz)", value=1.0)
        freq_max = st.number_input("Enter Max Frequency (MHz)", value=10.0)

    cap_min_pf = st.number_input("Capacitor Min Value (pF)", value=10.0)
    cap_max_pf = st.number_input("Capacitor Max Value (pF)", value=100.0)
    wire_diameter_mm = st.number_input("Copper Wire Diameter (mm)", value=0.5)

    def calculate_inductance(freq_mhz, cap_pf):
        f_hz = freq_mhz * 1e6
        c_f = cap_pf * 1e-12
        L = 1 / ((2 * math.pi * f_hz) ** 2 * c_f)
        return L * 1e6  # µH

    def wheeler(inductance_uh, wire_d_mm):
        wire_d_in = wire_d_mm / 25.4
        for d_in in [i * 0.1 for i in range(2, 20)]:
            for n in range(2, 100):
                l_in = n * wire_d_in
                L = (d_in ** 2 * n ** 2) / (18 * d_in + 40 * l_in)
                if abs(L - inductance_uh) < 0.1:
                    return {
                        "Turns": n,
                        "Diameter (mm)": round(d_in * 25.4, 2),
                        "Length (mm)": round(l_in * 25.4, 2)
                    }
        return None

    if st.button("🔍 Calculate"):
        L_max = calculate_inductance(freq_min, cap_max_pf)
        L_min = calculate_inductance(freq_max, cap_min_pf)

        st.markdown(f"### Inductance Range: `{round(L_min, 2)} µH` to `{round(L_max, 2)} µH`")

        coil_min = wheeler(L_min, wire_diameter_mm)
        coil_max = wheeler(L_max, wire_diameter_mm)

        st.markdown("#### 📐 Coil for L_min:")
        st.write(coil_min if coil_min else "Couldn't find a match.")

        st.markdown("#### 📐 Coil for L_max:")
        st.write(coil_max if coil_max else "Couldn't find a match.")

# ============================ TOOL 2: PATCH ANTENNA ============================
elif st.session_state.tool == "patch":
    st.subheader("📡 Microstrip Patch Antenna Calculator")

    f = st.number_input("Enter Frequency (GHz)", value=2.4)
    er = st.number_input("Dielectric Constant (εr)", value=4.4)
    h = st.number_input("Substrate Height h (mm)", value=1.6)

    if st.button("📏 Calculate Patch Dimensions"):
        c = 3e8
        h_m = h / 1000  # mm to meters
        fr = f * 1e9

        # Effective dielectric constant
        e_eff = (er + 1)/2 + (er - 1)/2 * (1 + 12 * h_m)**-0.5

        # Patch width
        W = c / (2 * fr * math.sqrt((er + 1)/2))

        # Extension length
        delta_L = h_m * 0.412 * ((e_eff + 0.3) * (W/h_m + 0.264)) / ((e_eff - 0.258) * (W/h_m + 0.8))

        # Effective length and actual length
        L_eff = c / (2 * fr * math.sqrt(e_eff))
        L = L_eff - 2 * delta_L

        st.markdown("### 📐 Patch Dimensions")
        st.write(f"Effective Dielectric Constant (ε_eff): `{round(e_eff, 4)}`")
        st.write(f"Patch Width (W): `{round(W * 1000, 2)} mm`")
        st.write(f"Patch Length (L): `{round(L * 1000, 2)} mm`")
