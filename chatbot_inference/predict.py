import numpy as np
import re
import torch
import random
from sklearn.preprocessing import LabelEncoder
from transformers import DistilBertTokenizer, DistilBertModel
import pathlib
import sys
import json
from transformers import logging
import os

scripts_dir = pathlib.Path(__file__).parent.resolve()
# model_path = os.path.join(scripts_dir, 'model.h5')
sys.path.append(str(scripts_dir))

from bert_model import BERT_Arch
from prerun import download_model_files
download_model_files()

default_intents_file = os.path.join(scripts_dir, 'intents.json')
default_model_file = os.path.join(scripts_dir, 'chatbot_model.pt')
default_responses_dict = os.path.join(scripts_dir, 'responses.json')

intents_file = os.environ.get('intents_file', default_intents_file)
model_file = os.environ.get('model_file', default_model_file)
responses_file = os.environ.get('responses_file', default_responses_dict)

# logging.set_verbosity_warning()
logging.set_verbosity_error()

# specify GPU
device = torch.device('cpu')

mode = os.environ.get('mode', 'intent')

if os.path.exists('/input/train'):
    model_path = '/input/train/chatbot_model.pt'
    intents_path = '/input/train/intents.json'

else:
    model_path = model_file
    intents_path = intents_file


f = open(intents_path)
intents = json.load(f)

    
number_of_labels = len(intents)

# Import the DistilBert pretrained model
model = BERT_Arch(DistilBertModel.from_pretrained('distilbert-base-uncased'), number_of_labels)

model.load_state_dict(torch.load(model_path))

if mode == 'response':
    f = open(responses_file)
    res = json.load(f)


def get_prediction(str):
    # Converting the labels into encodings
    le = LabelEncoder()
    lst = []
    for i in intents:
        lst = lst + [i]
    lst = le.fit_transform(lst)
    str = re.sub(r'[^a-zA-Z ]+', '', str)
    test_text = [str]
    model.eval()
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    tokens_test_data = tokenizer(test_text, max_length=8, padding='max_length',
                                 truncation=True, return_token_type_ids=False)
    test_seq = torch.tensor(tokens_test_data['input_ids'])
    test_mask = torch.tensor(tokens_test_data['attention_mask'])
    with torch.no_grad():
        preds = model(test_seq.to(device), test_mask.to(device))
    sm = torch.nn.Softmax(dim=1)
    probabilities = sm(preds)
    preds = preds.detach().cpu().numpy()
    preds = np.argmax(preds, axis=1)
    print(le.inverse_transform(preds)[0], probabilities[0][preds][0].item())
    return le.inverse_transform(preds)[0], probabilities[0][preds][0].item()

def get_response(data):
    message = data['input_text']
    print(message)
    intent, confidence = get_prediction(message)
    if mode == 'intent':
        result = {"intent": intent, "confidence": confidence}
        print(result)
        return result
    for i in res:
        if i == intent:
            result = random.choice(res[i])
            break
    result = {"intent": intent, "response": result, "confidence": confidence}
    print(result)
    return result