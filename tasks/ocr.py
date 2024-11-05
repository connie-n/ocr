
import requests, base64
import json
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import os

from tasks.utils.functions import parse_receipt_text
from transformers import pipeline


def load_model():
    return pipeline("image-to-text", model="jinhybr/OCR-Donut-CORD")


pipe = load_model()


def main():
    load_dotenv()
    
    stream = True

    st.title("Optical Character Recognition (OCR) with OCR-Donut-CORD")

    with open("./tasks/utils/description/ocr_description.txt", "r") as file:
        description = file.read()
    st.markdown(description)
    
    sample_image_path = "tasks/utils/sample/sample_recipt.png"
    sample_image = Image.open(sample_image_path)
    st.image(sample_image, caption="Sample Receipt Image", use_column_width=True)

    if st.button("Process"):
        with st.spinner("======== Sending request to API.. ========"):
            output = pipe(sample_image)
            st.write(output)

            extracted_text = output[0]["generated_text"]
            items, subtotal, tax, total = parse_receipt_text(extracted_text)
            st.header("Rewriting Model Results")
            st.write(
                """
                The model inference results show that it outputs the items and prices from the receipt image in JSON format. 
                For easier visibility, the items and prices are organized separately below. 
                While the tested OCR model demonstrates good text extraction, 
                it seems crucial to consider how to organize and display the extracted information, 
                as the format of receipts can vary widely in real life.
                """
            )
            st.subheader("Items and Prices:")
            for item, price in items:
                st.write(f"{item}: ${price}")

            st.subheader("Subtotal:")
            st.write(f"Subtotal: ${subtotal}")
            st.write(f"Tax: ${tax}")
            st.write(f"Total: ${total}")


    st.header("💡 Try with your receipt file")
    st.write(
            """
            Try testing the model with your own receipt image. 
            The model’s output will be displayed in JSON format as well. 
            To extract specific details in a desired format, you may need to implement additional code for further customization.
            Image file can available only in jpeg, jpg, png format. 
            """
            )

    uploaded_file = st.file_uploader("Upload an image", type=["jpeg", "jpg", "png"])

    print("Opening image file...")

    if uploaded_file is not None:
      image = Image.open(uploaded_file)
      st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

      if st.button("Process"):
          with st.spinner("======== Sending request to API.. ========"):          
              output = pipe(image)
              st.write(output)

              
                
