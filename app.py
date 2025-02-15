import os
import shutil
import streamlit as st
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
import mimetypes
from PIL import Image

CAPTURE_FOLDER = "files"

# loading all the environment variables
load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_ID = "gemini-2.0-flash"

def generate_response(client, model_id, contents):
    response = client.models.generate_content(
    model=model_id,
    contents=contents
    )
    return response



def detect_file_type(file_path):
    # Detect MIME type
    mime_type, _ = mimetypes.guess_type(file_path)

    # Check if the file is an image
    image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp']
    if mime_type in image_types:
        return 'image'

    # Check if the file is a PDF
    if mime_type == 'application/pdf':
        return 'pdf'


def remove_files_in_folder(folder_path):
    """Helper function to remove all contents of a folder path given by parameter `folder_path`"""
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")


def main():
    st.title("Chat with LLM")

    # Initial dropdown
    chat_type = st.selectbox("What would you like to chat with?", ["Text", "File"])

    if chat_type == "Text":
        # Text input and submit button
        text_input = st.text_area("Enter your text")
        submit_button = st.button("Submit")

        if submit_button:
            with st.spinner("Processing..."):
                start_time = time.time()
                output = generate_response(client, MODEL_ID, text_input)
                end_time = time.time()
                st.write("Output:")
                st.write(f"{output.text}")
                st.write(f"Time taken: {end_time - start_time} seconds")

    elif chat_type == "File":
        # File uploader
        file_uploader = st.file_uploader("Upload a file")
        file_uploaded = False
        uploaded_file = None

        if file_uploader:
            remove_files_in_folder(CAPTURE_FOLDER)

            with st.spinner("Uploading file..."):
                time.sleep(1)  # Simulate file upload time

                # Create a directory to store the uploaded file
                if not os.path.exists(CAPTURE_FOLDER):
                    os.makedirs(CAPTURE_FOLDER)

                # Save the uploaded file
                uploaded_file_path = os.path.join(CAPTURE_FOLDER, file_uploader.name)
                with open(uploaded_file_path, "wb") as f:
                    f.write(file_uploader.getbuffer())


                st.success("File uploaded successfully!")
                file_uploaded = True


        if file_uploaded:

            # Check what is the type of file and load appropriately.
            file_type = detect_file_type(uploaded_file_path)

            if file_type == "image" :

                image = Image.open(uploaded_file_path)
                image.thumbnail([512,512])
                st.image(image, caption="Uploaded Image.", use_container_width=True)


                # Text input for question
                question_input = st.text_area("Enter your question about the image")
                ask_button = st.button("Ask")

                if ask_button:
                    with st.spinner("Processing..."):
                        start_time = time.time()
                        output = generate_response(client, MODEL_ID, [question_input,image])

                        end_time = time.time()
                        st.write("Output:")
                        st.write(f"{output.text}")
                        st.write(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
