# Multi-Modal-Chat-App

Application on Streamlit to chat with any Text, Image, Audio, Document Inputs.
The following formats are supported by this application:

*Document formats:*

- PDF - application/pdf
- JavaScript - application/x-javascript, text/javascript
- Python - application/x-python, text/x-python
- TXT - text/plain
- HTML - text/html
- CSS - text/css
- Markdown - text/md
- CSV - text/csv
- XML - text/xml
- RTF - text/rtf


*Images:*

- PNG - image/png
- JPEG - image/jpeg
- WEBP - image/webp
- HEIC - image/heic
- HEIF - image/heif

*Audio:*

- WAV - audio/wav
- MP3 - audio/mp3
- AIFF - audio/aiff
- AAC - audio/aac
- OGG Vorbis - audio/ogg
- FLAC - audio/flac

## Setup

This project is initialized using `pdm`. To learn more about `pdm`, please refer to the [pdm documentation](https://pdm-project.org/en/latest/).

### Installation Steps

1. **Install `pdm`**:
    ```sh
    pip install pdm
    ```

2. **Initialize the project**:
    ```sh
    pdm init
    ```

3. **Install the required dependencies**:
    ```sh
    pdm install
    ```

4. **Create a [.env](http://_vscodecontentref_/2) file** in the root of your repository and include the following:
    ```env
    GOOGLE_API_KEY=<YOUR_API_KEY>
    ```

## Running the Application

To run the Streamlit application, use the following command:
```sh
pdm run streamlit run app.py
```

## References

- [Google API Docs](https://ai.google.dev/gemini-api/docs/document-processing?lang=python)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Dotenv Documentation](https://saurabh-kumar.com/python-dotenv/)
- [Pillow (PIL Fork) Documentation](https://pillow.readthedocs.io/en/stable/)
- [Mimetypes Module Documentation](https://docs.python.org/3/library/mimetypes.html)
- [PDM Documentation](https://pdm-project.org/)
