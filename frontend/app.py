import streamlit as st
import requests

st.title("ID Card OCR Application")
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Extracting text...")

    # Send the image to the FastAPI backend
    response = requests.post("http://localhost:8000/extract-text/", files={"file": uploaded_file})

    if response.status_code == 200:
        extracted_text = response.json().get("extracted_text")
        st.write("Extracted Text:")
        st.write(extracted_text)
    else:
        st.error("Error extracting text: " + response.text)