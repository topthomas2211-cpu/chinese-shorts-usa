import streamlit as st
from ui.app_ui import render_app

st.set_page_config(page_title="Chinese → USA Shorts V2", page_icon="🎬", layout="wide")
render_app()
