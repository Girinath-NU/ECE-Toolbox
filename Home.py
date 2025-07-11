import streamlit as st

st.set_page_config(page_title="Electronics Toolbox", layout="wide")

st.title("🧰 Electronics Toolbox")
st.markdown("Choose a tool to continue:")

# Create three columns for tools
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📻\nLC Tuning", use_container_width=True):
        from lc_tuner import main as lc_main
        lc_main()

with col2:
    if st.button("📡\nPatch Antenna", use_container_width=True):
        from patch_antenna import main as patch_main
        patch_main()

with col3:
    if st.button("🔴\nResistor Code", use_container_width=True):
        from resistor_color_code import main as resistor_main
        resistor_main()
