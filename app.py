
import requests, base64
import json
import streamlit as st
from dotenv import load_dotenv
import os


from tasks import image_captioning, ocr




add_task = st.sidebar.radio(
    "Which task would you like to try?",
    ("OCR", "Image Captioning")
)

if add_task == "OCR":
    ocr.main()

if add_task == "Image Captioning":
    image_captioning.main()





