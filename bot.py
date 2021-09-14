import nltk
from nltk.stem. lancaster import LancasterStemmer
stemmer = LancasterStemmer()

from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.models import model_from_yaml

import re
import numpy
import tflearn
import tensorflow
import random
import json
import os
import pandas as pd
import pickle
import numpy
import tflearn
import random
import json

import maya
from maya import MayaInterval

from datetime import datetime
from dateutil.parser import parse



nltk.download('punkt')
with open("intents.json",encoding="utf8") as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []
  
for intents in data["intents"]:
    for pattern in intents["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intents["tag"])

    if intents["tag"] not in labels:
        labels.append(intents["tag"])

words = [stemmer.stem(w.lower()) for w in words if w !="?"]
words = sorted(list(set(words)))

labels = sorted(labels)

train = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w) for w in doc]
    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)
    output_row =  out_empty[:]
    output_row[labels.index(docs_y[x])]=1
        
    train.append(bag)
    output.append(output_row)

train = numpy.array(train)
output = numpy.array(output)


net = tflearn.input_data(shape=[None,len(train[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net, len(output[0]),activation ="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)



model.fit(train,output, n_epoch=500, batch_size = 8, show_metric = True)
model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(words.lower()) for words in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag) 

def chatWithBot(inputText):
    global responded_A

    greetings = ("hi","hey","hello","start","i need help","help")
    conduct = ("yes","help me conduct a consultant","yes i do","i do")
 
    currentText = bag_of_words(inputText,words)
    currentTextArray =[currentText]
    numpyCurrentText = numpy.array(currentTextArray)

    
   
   
    results = model.predict(numpyCurrentText[0:1])
    results_index =numpy.argmax(results)
    tag = labels[results_index]

    if results[0][results_index] > 0.5:
        for tg in data["intents"]:
            if tg["tag"] == tag:
                responses = tg["responses"]
        return(random.choice(responses))
    
    elif inputText in greetings:
        now = maya.MayaDT.from_datetime(datetime.utcnow())
        Time_zone = now.hour +3

        if 5<= Time_zone <12 :
            Good_Morning="Good Morning"
            reply_greetings =("{}🌅 \nWelcome to Nav Healthcare Services"
                            "\nI am Paz😇, a Healthcare bot.\nI am here to help you navigate around our interface."
                            "\n\nFirst, what's your name?"
                            "\n\n(Information shared is end-to-end encrypted.No one outside the chat can read them.)"
            ).format(Good_Morning)
            
            responded_A = True
            #media = ('https://i.ibb.co/vw33c6C/Navv.png')

            return(reply_greetings)

           

            
        elif  12 <= Time_zone < 17 :
            Good_Afternoon="Good Afternoon"
            reply_greetings =("{}🌄\nWelcome to Nav Healthcare Services"
                            "\nI am Paz😇, a Healthcare bot.\nI am here to help you navigate around our interface."
                            "\n\nFirst, what's your name?"
                            "\n\n(Information shared is end-to-end encrypted.No one outside the chat can read them.)"
            ).format(Good_Afternoon)

            responded_A = True
            
            return(reply_greetings)
            #resp.

            
            
        else:
            Good_Evening="Good Evening"
            reply_greetings =("{}🌆 \nWelcome to Nav Healthcare Services"
                            "\nI am Paz😇, a Healthcare bot.\nI am here to help you navigate around our interface."
                            "\n\nFirst, what's your name?"
                            "\n\n(Information shared is end-to-end encrypted.No one outside the chat can read them.)"
            ).format(Good_Evening)

            responded_A = True
        

            return(reply_greetings)

            
    elif responded_A == True:
        
        global name
        name = inputText
        if not re.match("^[A-z][A-z|\.|\s]+$",name):
            reply_v = ("Please give a vallid name ^Example james^")
            return (reply_v)

        elif len(name) >10:
            reply_v = ("Kindly give your realistic name!!")
            return(reply_v)
        else:

            need=("Hey👋 {}\n\nWe are happy to have you 😍.I can help you in the following ways.\n\n   📝 Registration (if you are a new patient) \n   🔒 Log in (if you are an existing patient) \n   🏥 Diagnosis" 
            ).format(name)

            responded_A = False
            return(need)
    elif inputText in conduct:
        return "Thats okay.First, if you are an existing customer you can log in, if not, Kindly register.\nAt home click *contact a consultant* and you will be direct to where you have to make a payment"     
        
    else:
        return "Take it easy on me😓, i am still learning.\n\nMosty ask questions related to the interface and i will give you an appropriate answer. Thanks😍"
       
    
def chat():
    print("start talking with the bot")
    while True:
        inp = input ("you: ")
        if inp.lower() == "quit":
            break

        print(chatWithBot(inp))
