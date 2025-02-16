import os
import pathlib
import shutil
import streamlit as st
import time
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
import mimetypes
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)

MODEL_ID = "gemini-2.0-flash"
CAPTURE_FOLDER = "files"
IMAGE_MIME_TYPES = ["image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"]
DOCUMENT_MIME_TYPES = [
    "application/pdf",
    "application/x-javascript",
    "text/javascript",
    "application/x-python",
    "text/x-python",
    "text/plain",
    "text/css",
    "text/md",
    "text/csv",
    "text/xml",
    "text/rtf",
]

AUDIO_MIME_TYPES = [
    "audio/wav",
    "audio/mp3",
    "audio/aiff",
    "audio/aac",
    "audio/ogg",
    "audio/flac",
]

# Load all the environment variables
load_dotenv()

# Ensure the API key is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

client = genai.Client(api_key=api_key)


def generate_response(client: genai.Client, model_id: str, contents):
    try:
        response = client.models.generate_content(model=model_id, contents=contents)
        return response
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return None


def detect_mime_type(file_path: str) -> str:
    """
    Detects the MIME type of a file.

    This function uses the `mimetypes` module to guess the MIME type
    of a file based on its file extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The detected MIME type, or None if unknown.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def read_file(filepath: str) -> types.Part:
    """
    Reads a file and converts its contents into a `Part` object.

    This helper function supports reading files of various MIME types,
    including documents, images, and audio files. The file's contents
    are read and wrapped in a `Part` object, which is required for
    interacting with the Google API.

    Args:
        filepath (str): The path to the file to be read.

    Returns:
        types.Part: A `Part` object containing the file's contents.
    """
    try:
        data_bytes = types.Part.from_bytes(
            data=pathlib.Path(filepath).read_bytes(),
            mime_type=detect_mime_type(filepath),
        )
        return data_bytes
    except Exception as e:
        logging.error(f"Error reading file {filepath}: {e}")
        return None


def read_image(filepath: str):
    try:
        image = Image.open(filepath)
        image.thumbnail([512, 512])
        return image
    except Exception as e:
        logging.error(f"Error reading image {filepath}: {e}")
        return None


def remove_files_in_folder(folder_path):
    """
    Removes all contents of a folder.

    This function deletes all files and subfolders within the specified
    folder path. If the folder does not exist, no action is taken.

    Args:
        folder_path (str): The path to the folder to be cleared.

    Raises:
        Exception: If an error occurs while deleting a file or folder.

    """
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error(f"Failed to delete {file_path}. Reason: {e}")


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
                if output:
                    st.write("Output:")
                    st.write(f"{output.text}")
                    st.write(f"Time taken: {end_time - start_time} seconds")
                else:
                    st.error("Failed to generate response")

    elif chat_type == "File":
        # File uploader
        file_uploader = st.file_uploader("Upload a file")
        file_uploaded = False

        if file_uploader:
            remove_files_in_folder(CAPTURE_FOLDER)

            with st.spinner("Uploading file..."):
                time.sleep(1)  # Simulate file upload time

                # Create a directory to store the uploaded file
                if not os.path.exists(CAPTURE_FOLDER):
                    os.makedirs(CAPTURE_FOLDER)

                # Save the uploaded file
                uploaded_file_path: str = os.path.join(
                    CAPTURE_FOLDER, file_uploader.name
                )
                try:
                    with open(uploaded_file_path, "wb") as f:
                        f.write(file_uploader.getbuffer())
                    st.success("File uploaded successfully!")
                    file_uploaded = True
                except Exception as e:
                    st.error(f"Failed to upload file: {e}")
                    logging.error(f"Failed to upload file: {e}")

        if file_uploaded:
            # Check what is the mime_type of file and load appropriately.
            mime_type = detect_mime_type(uploaded_file_path)
            if (
                mime_type
                not in DOCUMENT_MIME_TYPES + AUDIO_MIME_TYPES + IMAGE_MIME_TYPES
            ):
                st.markdown(
                    f"Unable to submit request because it has a mimeType parameter with value {mime_type}, which is not supported. Update the mimeType and try again."
                )
            else:
                content = read_file(uploaded_file_path)

                if mime_type in IMAGE_MIME_TYPES:
                    st.image(
                        read_image(uploaded_file_path),
                        caption="Uploaded Image.",
                        use_container_width=True,
                    )

                # Text input for question
                question_input = st.text_area(
                    f"Enter your question about the {mime_type}"
                )
                ask_button = st.button("Ask")

                if ask_button:
                    with st.spinner("Processing..."):
                        start_time = time.time()
                        output = generate_response(
                            client, MODEL_ID, [question_input, content]
                        )

                        end_time = time.time()
                        if output:
                            st.write("Output:")
                            st.write(f"{output.text}")
                            st.write(f"Time taken: {end_time - start_time} seconds")
                        else:
                            st.error("Failed to generate response")


if __name__ == "__main__":
    main()
