import streamlit as st
from PIL import Image

st.set_page_config(page_title="Electronics Toolbox", layout="centered")

st.title("🔧 Electronics Toolbox")
st.subheader("Your go-to toolkit for core electronics design & calculation")

st.markdown("---")
st.markdown("### 🚀 Available Tools:")
st.markdown("- 🌀 **LC Tuning Circuit Designer** (in sidebar)")
st.markdown("- 📡 **Microstrip Patch Antenna Calculator** (in sidebar)")
st.markdown("- 🛠️ More tools coming soon!")

st.markdown("---")
st.markdown("Made with ❤️ by [Girinath NU](https://github.com/girinath-nu)")

image = Image.open("your_logo_or_banner.png")
st.image(image, caption="Explore. Calculate. Build.", use_column_width=True)
