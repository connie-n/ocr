
import requests, base64
import json
import streamlit as st
from dotenv import load_dotenv
import os


from palligemma import image_captioning, ocr




add_selectbox = st.sidebar.selectbox(
    "Which task would you like to try?",
    ("Image Captioning", "OCR")
)

if add_selectbox == "Image Captioning":
    image_captioning.main()

if add_selectbox == "OCR":
    ocr.main()



