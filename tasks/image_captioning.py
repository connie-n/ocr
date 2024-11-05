
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

    with open("./palligemma/description.txt", "r") as file:
        description = file.read()

    st.title("Image Captioning with Paligemma")

    st.markdown(description)



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

        if st.button("Generate Caption"):
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
                st.write("Generated Caption:")
                st.write(caption)
            else:
                st.error(f"Error: {response.status_code}")

    else:
        if not Palligemma_api_key:
            st.error("API key not found. Please check your .env file.")
        else:
            st.warning("Please upload an image.")

  # sample_image
    st.markdown("If you don't have image file, try to use the sample image provided after saving and loading it:")
    sample_image_path = "./palligemma/sample_image_dog.jpeg"
    if os.path.exists(sample_image_path):
        st.image(sample_image_path, caption='Sample Image', use_column_width=True)
        # if st.button("Generate Caption for Sample Image"):
        #     with open(sample_image_path, "rb") as img_file:
        #         image_b64 = base64.b64encode(img_file.read()).decode()

        #    generate_caption(image_b64, Palligemma_api_key, invoke_url, stream)
    else:
        st.error("Sample image not found. Please ensure the sample image is in the correct directory.")










