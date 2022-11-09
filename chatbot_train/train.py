import numpy as np
import pandas as pd
import re
import torch
import torch.nn as nn
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizer, DistilBertModel
from torch.utils.data import TensorDataset, DataLoader, RandomSampler
from torchinfo import summary
from transformers import AdamW
from sklearn.utils.class_weight import compute_class_weight
from bert_model import BERT_Arch
from transformers import logging
import os
import json
import argparse
from binaryornot.check import is_binary


cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")

#logging.set_verbosity_warning()
logging.set_verbosity_error()

# specify GPU
device = torch.device("cpu")
parser = argparse.ArgumentParser(description="""Preprocessor""")


parser.add_argument('--data', action='store', dest='data', required=False,default='messages.csv',
                    help="""string. csv file name for training data""")


parser.add_argument('--epochs', action='store', dest='epochs', default=5,
                    help="""string. csv file name for training data""")

args = parser.parse_args()
data = args.data
epochs_count = int(args.epochs)
epochs = epochs_count
train_losses = []
train_loss = ""
model = ""

def train(data):
    df = pd.read_csv(data)
    global model    
    labels_list = list(set(df['intent']))

    with open('intents.json', 'w') as outfile:
        json.dump(labels_list, outfile)

    # Converting the labels into encodings
    le = LabelEncoder()
    df['intent'] = le.fit_transform(df['intent'])

    x_train, x_test, y_train, y_test = train_test_split(df['text'], df['intent'], test_size=0.2, random_state=42)

    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    # Import the DistilBert pretrained model
    bert = DistilBertModel.from_pretrained('distilbert-base-uncased')

    # tokenize and encode sequences in the training set
    tokens_train = tokenizer(
        x_train.tolist(),
        max_length = 8,
        padding='max_length',
        truncation=True,
        return_token_type_ids=False)

    # tokenize and encode sequences in the test set
    tokens_test = tokenizer(
        x_test.tolist(),
        max_length = 8,
        padding='max_length',
        truncation=True,
        return_token_type_ids=False)

    # for train set
    train_seq = torch.tensor(tokens_train['input_ids'])
    train_mask = torch.tensor(tokens_train['attention_mask'])
    train_y = torch.tensor(y_train.tolist())

    # for test set
    test_seq = torch.tensor(tokens_test['input_ids'])
    test_mask = torch.tensor(tokens_test['attention_mask'])
    test_y = torch.tensor(y_test.tolist())


    #define a batch size
    batch_size = 16
    # wrap tensors
    train_data = TensorDataset(train_seq, train_mask, train_y)
    test_data = TensorDataset(test_seq, test_mask, test_y)
    # sampler for sampling the data during training
    train_sampler = RandomSampler(train_data)
    test_sampler = RandomSampler(test_data)

    # DataLoader for train set
    train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)
    # DataLoader for test set
    test_dataloader = DataLoader(test_data, sampler=test_sampler, batch_size=batch_size)

    # freeze all the parameters. This will prevent updating of model weights during fine-tuning.
    for param in bert.parameters():
        param.requires_grad = False
    model = BERT_Arch(bert, len(labels_list))
    # push the model to GPU
    model = model.to(device)
    summary(model)

    # define the optimizer
    optimizer = AdamW(model.parameters(), lr = 1e-3)

    #compute the class weights
    class_wts = compute_class_weight('balanced', np.unique(y_train), y_train)
    #print(class_wts)

    # convert class weights to tensor
    weights= torch.tensor(class_wts,dtype=torch.float)
    weights = weights.to(device)
    # loss function
    cross_entropy = nn.NLLLoss(weight=weights) 

    # empty lists to store training and validation loss of each epoch
    train_losses=[]
    test_losses=[]
    # number of training epochs
    
    #
    # print(labels_list)

    model.train()
    train_total_loss = 0
    train_correct = 0
    test_total_loss = 0
    test_correct = 0
    # empty list to save model predictions
    total_preds=[]
    # iterate over batches
    for step,batch in enumerate(train_dataloader):  
        # progress update after every 50 batches.
        if step % 50 == 0 and not step == 0:
            print('  Batch {:>5,}  of  {:>5,}.'.format(step, len(train_dataloader)))
        # push the batch to gpu
        batch = [r.to(device) for r in batch] 
        sent_id, mask, labels = batch
        # get model predictions for the current batch
        preds = model(sent_id, mask)
        # compute the loss between actual and predicted values
        loss = cross_entropy(preds, labels)
        # add on to the total loss
        train_total_loss = train_total_loss + loss.item()
        # backward pass to calculate the gradients
        loss.backward()
        # clip the the gradients to 1.0. It helps in preventing the exploding gradient problem
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        # update parameters
        optimizer.step()
        int_preds = np.argmax(preds.detach().cpu().numpy(), axis = 1)
        for a,b in zip(int_preds, labels.detach().cpu().numpy()):
            if a == b:
                train_correct += 1
        # clear calculated gradients
        optimizer.zero_grad()
        # model predictions are stored on GPU. So, push it to CPU
        preds=preds.detach().cpu().numpy()
        # append the model predictions
        total_preds.append(preds)
    # compute the training loss of the epoch
    train_avg_loss = train_total_loss / len(train_dataloader)
    train_accuracy = 100 * train_correct / len(x_train)
    # predictions are in the form of (no. of batches, size of batch, no. of classes).
    # reshape the predictions in form of (number of samples, no. of classes)
    total_preds  = np.concatenate(total_preds, axis=0)
    #returns the loss and predictions
    print("Train Acc:")
    print(train_accuracy)
    total_preds_test=[]
    model.eval()     # Optional when not using Model Specific layer
    for step, batch in enumerate(test_dataloader):  
        batch = [r.to(device) for r in batch] 
        sent_id, mask, labels = batch
        # get model predictions for the current batch
        preds = model(sent_id, mask)
        # compute the loss between actual and predicted values
        loss = cross_entropy(preds, labels)
        # add on to the total loss
        train_total_loss = train_total_loss + loss.item()
        int_preds = np.argmax(preds.detach().cpu().numpy(), axis = 1)
        for a,b in zip(int_preds, labels.detach().cpu().numpy()):
            if a == b:
                test_correct += 1
        # model predictions are stored on GPU. So, push it to CPU
        preds=preds.detach().cpu().numpy()
        # append the model predictions
        total_preds_test.append(preds)
        
    # compute the training loss of the epoch
    test_avg_loss = test_total_loss / len(test_dataloader)
    test_accuracy = 100 * test_correct / len(x_test)
    # predictions are in the form of (no. of batches, size of batch, no. of classes).
    # reshape the predictions in form of (number of samples, no. of classes)
    total_preds  = np.concatenate(total_preds, axis=0)
    #returns the loss and predictions
    print("Test Acc:")
    print(test_accuracy)

    return train_avg_loss, train_accuracy, test_avg_loss, test_accuracy, total_preds
def train_run(df1="messages.csv",epochs=2):
    with open(df1, 'rb') as f:
        for block in f:
            if b'\0' in block:
                return False
    if epochs < 1 or df1 =="" or epochs > 250 or os.stat(df1).st_size == 0:
        return False
    else:
        for epoch in range(epochs):
            print('\n Epoch {:} / {:}'.format(epoch + 1, epochs))
            #train model
            train_loss, train_accuracy, test_loss, test_accuracy, total_preds = train(df1)
            # append training and validation loss
            train_losses.append(train_loss)
            
            # it can make your experiment reproducible, similar to set  random seed to all options where there needs a random seed.
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
            
        print(f'\nTraining Loss: {train_loss:.3f}')
        print(f'\nTraining Accuracy: {train_accuracy:.3f}')
        print(f'\nTest Accuracy: {test_accuracy:.3f}')

        torch.save(model.state_dict(), "chatbot_model.pt")
        return True
