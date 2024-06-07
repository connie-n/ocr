
import requests, base64
import json
import streamlit as st
from streamlit.script_runner import RerunException
from dotenv import load_dotenv
import os


import palligemma.image_captioning


selected_menu = st.sidebar.selectbox("Select Task", ("Image Captioning", "OCR"))

if selected_menu == "Image Captioning":
    try:
        image_captioning.main()
    except RerunException:
        pass
elif selected_menu == "OCR":
    try:
        image_captioning.main()
    except RerunException:
        pass




