import requests
import os
import pathlib


def download_model_files():
    current_dir = pathlib.Path(__file__).parent.resolve()
    if not os.path.exists(str(current_dir) + '/chatbot_model.pt') and not os.path.exists('input/train/chatbot_model.pt'):
        MODEL_FILE_URL = "https://blueprints-data.s3.us-west-2.amazonaws.com/model_files/chatbot/chatbot_model.pt"
        print('Downloading Model Files...')
        response = requests.get(MODEL_FILE_URL)
        open("chatbot_model.pt", "wb").write(response.content)
        print('Model Files Downloaded!')
