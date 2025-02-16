# Multi-Modal-Chat-App

Application on Streamlit to chat with any Text, Image, Audio, Document Inputs. 

*NOTE:* Here we can chat with only 1 document at a time

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

This project is initialized using `pdm`. To learn more about `pdm` please refer to [pdm documentation](https://pdm-project.org/en/latest/)

- Install `pdm` using the command: `pip install pdm`
- Then initialize a blank project using the command `pdm init`. This will provide a bunch of prompts to fill, after which a template is created for you.


## Requirements

We require 3 libraries to run this project
- `streamlit`: For creating our frontend application
- `google-genai`: For using Google's LLMs (Like Google Pro, Google Flash models)
- `python-dotenv`: Used to load `.env` files

- You will have to create a `.env` file in the root of your repo and include the following

`GOOGLE_API_KEY = <YOUR_API_KEY>`

## Executing the project

- After installing the required packages, run `pdm run streamlit run app.py` to run the streamlit app.

## References

- [Google API Docs](https://ai.google.dev/gemini-api/docs/document-processing?lang=python)
