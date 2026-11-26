import streamlit as st
from app.interface import render_app

st.set_page_config(
    page_title="Colour Space Converter",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_app()
