
import requests, base64
import json
import streamlit as st
from dotenv import load_dotenv
import os



def main():
    load_dotenv()



    Palligemma_api_key = os.getenv("Paligemma_API")

    invoke_url = "https://ai.api.nvidia.com/v1/vlm/google/paligemma"
    stream = True


    st.title("Optical Character Recognition (OCR) with Paligemma")
    uploaded_file = st.file_uploader("Upload an image", type=["jpeg", "jpg", "png"])

    print("Opening image file...")


    if uploaded_file is not None and Palligemma_api_key:
        
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        
        image_b64 = base64.b64encode(uploaded_file.read()).decode()

        assert len(image_b64) < 180_000, \
          "To upload larger images, use the assets API (see docs)"
        
        headers = {
          "Authorization": f"Bearer {Palligemma_api_key}",
          "Accept": "text/event-stream"
        }


        payload = {
          "messages": [
            {
              "role": "user",
              "content": f'Describe the image. <img src="data:image/jpeg;base64,{image_b64}" />'
            }
          ],
          "max_tokens": 512,
          "temperature": 1.00,
          "top_p": 0.70,
          "stream": stream
        }

        if st.button("Process"):
            st.write("======== Sending request to API.. ========")
            response = requests.post(invoke_url, headers=headers, json=payload)

            if response.status_code == 200:
                st.write("======== Processing stream response... ========")
                caption = ""
                for line in response.iter_lines():
                    if line:
                        data_str = line.decode("utf-8")
                        if data_str.startswith("data: "):
                            data_str = data_str[len("data: "):]
                            if data_str.strip() != "[DONE]":
                                data_json = json.loads(data_str)
                                content = data_json['choices'][0]['delta'].get('content', '')
                                if content:
                                    caption += content
                st.write("Extracted Text:")
                st.write(caption)
            else:
                st.error(f"Error: {response.status_code}")


    else:
        if not Palligemma_api_key:
            st.error("API key not found. Please check your .env file.")
        else:
            st.warning("Please upload an image.")









