
import requests, base64
import json
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import os

from transformers import pipeline



def load_model():
    return pipeline("image-to-text", model="jinhybr/OCR-Donut-CORD")

pipe = load_model()

def main():
    load_dotenv()
    
    stream = True

    st.title("Optical Character Recognition (OCR) with OCR-Donut-CORD")
    uploaded_file = st.file_uploader("Upload an image", type=["jpeg", "jpg", "png"])


    print("Opening image file...")

    if uploaded_file is not None:
      image = Image.open(uploaded_file)
      st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

      if st.button("Process"):
          with st.spinner("======== Sending request to API.. ========"):
              output = pipe(image)
              st.write(output)
        








