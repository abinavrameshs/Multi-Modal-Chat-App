import os
import shutil
import streamlit as st
import time

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
                # model = load_model()
                # output = model(text_input, max_length=512)
                output = "OUTPUT GENERATED"
                end_time = time.time()
                st.write("Output:")
                st.write(f"{text_input}-{output}")
                st.write(f"Time taken: {end_time - start_time} seconds")
                
    elif chat_type == "File":
        # File uploader
        file_uploader = st.file_uploader("Upload a file")
        file_uploaded = False
        uploaded_file = None
        
        if file_uploader:
            remove_files_in_folder("files")

            with st.spinner("Uploading file..."):
                time.sleep(1)  # Simulate file upload time
                
                # Create a directory to store the uploaded file
                if not os.path.exists("files"):
                    os.makedirs("files")
                
                # Save the uploaded file
                uploaded_file_path = os.path.join("files", file_uploader.name)
                with open(uploaded_file_path, "wb") as f:
                    f.write(file_uploader.getbuffer())
                uploaded_file = uploaded_file_path
                
                st.success("File uploaded successfully!")
                file_uploaded = True

        
        if file_uploaded:
                # Text input for question
                question_input = st.text_area("Enter your question about the file")
                ask_button = st.button("Ask")
                
                if ask_button:
                    with st.spinner("Processing..."):
                        start_time = time.time()
                        output = "OUTPUT GENERATED"
                        
                        end_time = time.time()
                        st.write("Output:")
                        st.write(f"{question_input}-{output}")
                        st.write(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()

