import streamlit as st

# Color code and values
color_codes = {
    "Black": (0, 1),
    "Brown": (1, 10),
    "Red": (2, 100),
    "Orange": (3, 1_000),
    "Yellow": (4, 10_000),
    "Green": (5, 100_000),
    "Blue": (6, 1_000_000),
    "Violet": (7, 10_000_000),
    "Gray": (8, 100_000_000),
    "White": (9, 1_000_000_000)
}

st.title("🎨 Resistor Color Code Calculator")

st.markdown("Select the resistor color bands to calculate resistance:")

col1, col2, col3 = st.columns(3)

with col1:
    band1 = st.selectbox("1st Band", color_codes.keys())
with col2:
    band2 = st.selectbox("2nd Band", color_codes.keys())
with col3:
    multiplier = st.selectbox("Multiplier", color_codes.keys())

def calc_resistance(b1, b2, mul):
    digit1 = color_codes[b1][0]
    digit2 = color_codes[b2][0]
    factor = color_codes[mul][1]
    resistance = ((digit1 * 10) + digit2) * factor
    return resistance

def format_resistance(value):
    if value >= 1_000_000:
        return f"{value/1_000_000:.2f} MΩ"
    elif value >= 1_000:
        return f"{value/1_000:.2f} KΩ"
    else:
        return f"{value:.2f} Ω"

resistance = calc_resistance(band1, band2, multiplier)
formatted = format_resistance(resistance)

st.success(f"Resistance: **{formatted} ± 20%**")

st.markdown("---")
st.caption("Supports 3-band resistor code. For more, stay tuned!")
