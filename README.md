# Multi-Modal-Chat-App

Application on Streamlit to chat with any Text and Image Inputs

## Setup

This project is initialized using `pdm`. To learn more about `pdm` please refer to [pdm documentation](https://pdm-project.org/en/latest/)

- Install `pdm` using the command `pip install pdm`
- Then initialize a blank project using the command `pdm init`. This will provide a bunch of prompts to fill, after which a template is created for you.


## Requirements

We require 3 libraries to run this project
- `streamlit` : For creating our frontend application
- `google-genai` : For using Google's LLMs (Like Google Pro, Google Flash models)
- `python-dotenv` : Used to load `.env` files

## Executing the project

- After installing the required packages, run `pdm run streamlit run app.py` to run the streamlit app.